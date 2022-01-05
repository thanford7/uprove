import logging
from datetime import datetime

from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp import security
from upapp.apis import setSkills
from upapp.modelSerializers import getSerializedProject, getSerializedProjectFunction, getSerializedProjectSkill
from upapp.models import Project, ProjectFunction, ProjectSkill, ProjectFile, ProjectInstructions, ProjectEvaluationCriterion
from upapp.utils import dataUtil


logger = logging.getLogger()


class ProjectView(APIView):

    def get(self, request, projectId=None):
        projectId = projectId or request.data['id']
        isPermittedSessionUser = security.isPermittedSessionUser(request)
        user = security.getSessionUser(request)
        employerId = user['employerId'] if user else None
        if projectId:
            return Response(getSerializedProject(self.getProject(projectId), isIncludeDetails=isPermittedSessionUser, evaluationEmployerId=employerId), status=status.HTTP_200_OK)

        employerId = request.data.get('employerId')
        return Response([getSerializedProject(p, isIncludeDetails=isPermittedSessionUser, evaluationEmployerId=employerId) for p in self.getProjects(employerId=employerId)])

    @atomic
    def post(self, request):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        project = Project(
            title=data['title'],
            image=data.get('image'),
            function_id=data['functionId'],
            skillLevelBits=data['skillLevelBits'],
            description=data['description'],
            background=data['background'],
            employer_id=data.get('employerId'),
            modifiedDateTime=datetime.utcnow(),
            createdDateTime=datetime.utcnow()
        )
        project.save()

        setSkills(project, data.get('skillIds'))
        self.setInstructions(project, data.get('instructions'))
        self.setEvaluationCriteria(project, data.get('evaluationCriteria'))
        self.setFiles(project, data.getlist('files', []), data.get('filesMetaData', []), request)

        return Response(status=status.HTTP_200_OK, data=getSerializedProject(self.getProject(project.id), isIncludeDetails=True, isAdmin=True))

    @atomic
    def put(self, request, projectId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        projectId = projectId or data['id']
        if not projectId:
            return Response('A project ID is required', status=status.HTTP_400_BAD_REQUEST)

        project = self.getProject(projectId)
        dataUtil.setObjectAttributes(project, data, {
            'title': None,
            'function_id': {'formName': 'functionId'},
            'skillLevelBits': None,
            'description': None,
            'background': None,
            'employer_id': {'formName': 'employerId'}
        })
        if image := data.get('image'):
            project.image = image

        isChanged = any([
            setSkills(project, data.get('skillIds')),
            self.setInstructions(project, data.get('instructions')),
            self.setEvaluationCriteria(project, data.get('evaluationCriteria')),
            self.setFiles(project, data.getlist('files', []), data.get('filesMetaData', []), request)
        ])

        if isChanged:
            project.modifiedDateTime = datetime.utcnow()

        project.save()
        return Response(status=status.HTTP_200_OK, data=getSerializedProject(self.getProject(project.id), isIncludeDetails=True, isAdmin=True))

    def delete(self, request, projectId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        projectId = projectId or request.data['id']
        if not projectId:
            return Response('A project ID is required', status=status.HTTP_400_BAD_REQUEST)

        project = self.getProject(projectId)
        project.delete()
        return Response(status=status.HTTP_200_OK, data=projectId)

    @staticmethod
    def getProject(projectId):
        try:
            return Project.objects \
                .select_related('employer', 'function') \
                .prefetch_related('evaluationCriteria', 'projectFile', 'projectInstructions', 'skills') \
                .get(id=projectId)
        except Project.DoesNotExist as e:
            raise e

    @staticmethod
    def getProjects(employerId=None, isIgnoreEmployerId=False, projectIds=None):
        if isIgnoreEmployerId:
            q = Q()
        else:
            q = Q(employer_id__isnull=True)
            if employerId:
                q |= Q(employer_id=employerId)
        if projectIds:
            q &= Q(id__in=projectIds)
        return Project.objects\
            .select_related('employer', 'function')\
            .prefetch_related('evaluationCriteria', 'projectFile', 'projectInstructions', 'skills')\
            .filter(q)

    @staticmethod
    def setFiles(project, files, filesMetaData, request):
        isChanged = False
        existingProjectFiles = {pf.id: pf for pf in ProjectFile.objects.filter(project_id=project.id)}
        filesDict = {f.name: f for f in files}
        usedProjectFileIds = []
        for metaData in filesMetaData:
            file = filesDict[metaData['fileKey']] if metaData['fileKey'] else None
            if not (projectFileId := metaData.get('id')):
                if not file:
                    raise ValueError(f'Must upload an actual file for title = {metaData["title"]}')
                projectFile = ProjectFile(
                    project=project,
                    title=metaData['title'],
                    description=metaData.get('description'),
                    skillLevelBits=metaData['skillLevelBits'],
                    file=file,
                    modifiedDateTime=datetime.utcnow(),
                    createdDateTime=datetime.utcnow()
                )
                projectFile.save()
                isChanged = True
            else:
                existingProjectFile = existingProjectFiles.get(projectFileId)
                if not existingProjectFile:
                    msg = f'No project file exists with ID = {projectFileId}'
                    logger.error(msg)
                    messages.error(request, msg)
                    continue

                usedProjectFileIds.append(projectFileId)
                isChanged = isChanged or dataUtil.setObjectAttributes(existingProjectFile, metaData, {
                    'title': None,
                    'description': None,
                    'skillLevelBits': None
                })
                if file:
                    existingProjectFile.file = file
                    existingProjectFile.modifiedDateTime = datetime.utcnow()
                existingProjectFile.save()

        deleteProjectFileIds = [id for id in existingProjectFiles.keys() if id not in usedProjectFileIds]
        if deleteProjectFileIds:
            isChanged = True
            ProjectFile.objects.filter(id__in=deleteProjectFileIds).delete()

        return isChanged

    @staticmethod
    def setInstructions(project, instructions):
        usedInstructionIds = []
        existingInstructions = {pi.id: pi for pi in ProjectInstructions.objects.filter(project=project)}
        isChanged = False
        for instruction in instructions:
            if existingInstruction := existingInstructions.get(instruction.get('id')):
                isChanged = isChanged or dataUtil.setObjectAttributes(existingInstruction, instruction, {
                    'instructions': None,
                    'skillLevelBit': None
                })
                existingInstruction.save()
                usedInstructionIds.append(instruction['id'])
            else:
                newInstruction = ProjectInstructions(
                    project=project,
                    instructions=instruction['instructions'],
                    skillLevelBit=instruction['skillLevelBit'],
                    modifiedDateTime=datetime.utcnow(),
                    createdDateTime=datetime.utcnow()
                )
                newInstruction.save()
                isChanged = True
        deleteInstructionIds = [id for id in existingInstructions.keys() if id not in usedInstructionIds]
        if deleteInstructionIds:
            isChanged = True
            ProjectInstructions.objects.filter(id__in=deleteInstructionIds).delete()

        return isChanged

    @staticmethod
    def setEvaluationCriteria(project, evaluationCriteria):
        usedCriteriaIds = []
        existingCriteria = {ec.id: ec for ec in ProjectEvaluationCriterion.objects.filter(project_id=project.id)}
        isChanged = False
        for criterion in (evaluationCriteria or []):
            if existingCriterion := existingCriteria.get(criterion.get('id')):
                isChanged = isChanged or dataUtil.setObjectAttributes(existingCriterion, criterion, {
                    'criterion': None,
                    'category': None,
                    'skillLevelBits': None,
                    'employer_id': {'formName': 'employerId'}
                })
                usedCriteriaIds.append(existingCriterion.id)
            else:
                newCriterion = ProjectEvaluationCriterion(
                    project_id=project.id,
                    criterion=criterion['criterion'],
                    category=criterion.get('category'),
                    skillLevelBits=criterion.get('skillLevelBits'),
                    employer_id=criterion.get('employerId')
                )
                newCriterion.save()
                isChanged = True

        deleteCriteriaIds = [id for id in existingCriteria.keys() if id not in usedCriteriaIds]
        if deleteCriteriaIds:
            isChanged = True
            ProjectEvaluationCriterion.objects.filter(id__in=deleteCriteriaIds).delete()

        return isChanged


class FunctionView(APIView):

    def post(self, request):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            projectFunction = ProjectFunction(functionName=request.data['functionName'])
            projectFunction.save()
            return Response(status=status.HTTP_200_OK, data=getSerializedProjectFunction(projectFunction))
        except IntegrityError as e:
            raise e

    def put(self, request, functionId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        functionId = functionId or request.data.get('id')
        if not functionId:
            return Response('A project function ID is required', status=status.HTTP_400_BAD_REQUEST)

        projectFunction = self.getProjectFunction(functionId)
        try:
            projectFunction.functionName = request.data['functionName']
            projectFunction.save()
            return Response(status=status.HTTP_200_OK, data=getSerializedProjectFunction(projectFunction))
        except IntegrityError as e:
            raise e

    def delete(self, request, functionId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        functionId = functionId or request.data.get('id')
        projectFunction = self.getProjectFunction(functionId)
        projectFunction.delete()
        return Response(status=status.HTTP_200_OK, data=functionId)

    @staticmethod
    def getProjectFunction(functionId):
        try:
            return ProjectFunction.objects.get(id=functionId)
        except ProjectFunction.DoesNotExist as e:
            raise e


class SkillView(APIView):

    def post(self, request):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            projectSkill = ProjectSkill(
                skillName=request.data['skillName'],
                instruction=request.data.get('instruction')
            )
            projectSkill.save()
            return Response(status=status.HTTP_200_OK, data=getSerializedProjectSkill(projectSkill))
        except IntegrityError as e:
            raise e

    def put(self, request, skillId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        skillId = skillId or request.data.get('id')
        if not skillId:
            return Response('A project skill ID is required', status=status.HTTP_400_BAD_REQUEST)

        projectSkill = self.getProjectSkill(skillId)
        try:
            dataUtil.setObjectAttributes(projectSkill, request.data, {
                'skillName': None,
                'instruction': None
            })
            projectSkill.save()
            return Response(status=status.HTTP_200_OK, data=getSerializedProjectSkill(projectSkill))
        except IntegrityError as e:
            raise e

    def delete(self, request, skillId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        skillId = skillId or request.data.get('id')
        projectSkill = self.getProjectSkill(skillId)
        projectSkill.delete()
        return Response(status=status.HTTP_200_OK, data=skillId)

    @staticmethod
    def getProjectSkill(skillId):
        try:
            return ProjectSkill.objects.get(id=skillId)
        except ProjectSkill.DoesNotExist as e:
            raise e
