import logging

from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.db.transaction import atomic
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp import security
from upapp.apis import UproveAPIView
from upapp.modelSerializers import getSerializedProject, getSerializedRole, getSerializedSkill, getAllowedProjects
from upapp.models import Project, Role, Skill, ProjectFile, ProjectEvaluationCriterion, CustomProject, EmployerJob
from upapp.utils import dataUtil


logger = logging.getLogger()


class ProjectView(UproveAPIView):

    def get(self, request, projectId=None):
        projectId = projectId or self.data.get('id')
        isPermittedSessionUser = security.isPermittedSessionUser(request)
        employerId = self.user.employer_id if self.user else None
        if projectId:
            return Response(getSerializedProject(self.getProject(projectId), isIncludeDetails=isPermittedSessionUser, evaluationEmployerId=employerId), status=status.HTTP_200_OK)

        employerId = int(self.data.get('employerId')[0])
        allowedProjectIds = None
        if jobId := self.data.get('jobId'):
            job = EmployerJob.objects.get(id=int(jobId[0]))
            customProjects = CustomProject.objects.select_related('project').all()
            allowedCustomProjects = getAllowedProjects(customProjects, job)
            allowedProjectIds = [p.project_id for p in allowedCustomProjects]

        return Response([
            getSerializedProject(p, isIncludeDetails=isPermittedSessionUser, evaluationEmployerId=employerId)
            for p in self.getProjects(employerId=employerId, projectIds=allowedProjectIds)
        ])

    @atomic
    def post(self, request):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        project = Project(createdDateTime=timezone.now())
        dataUtil.setObjectAttributes(project, self.data, {
            'title': None,
            'image': None,
            'role_id': {'formName': 'roleId'},
            'skillLevelBit': None,
            'description': None,
            'background': None,
            'instructions': None,
            'employer_id': {'formName': 'employerId'},
        })
        project.save()

        try:
            SkillView.setProjectSkills(project, self.data.get('skills'))
        except ValueError as e:
            return Response(status=status.HTTP_409_CONFLICT, data=e.__str__())
        self.setEvaluationCriteria(project, self.data.get('evaluationCriteria'))
        self.setFiles(project, self.files.get('files', []), self.data.get('filesMetaData', []), request)
        self.createOrUpdateCustomProject(project)

        return Response(status=status.HTTP_200_OK, data=getSerializedProject(self.getProject(project.id), isIncludeDetails=True, isAdmin=True))

    @atomic
    def put(self, request, projectId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        projectId = projectId or self.data['id']
        if not projectId:
            return Response('A project ID is required', status=status.HTTP_400_BAD_REQUEST)

        project = self.getProject(projectId)
        dataUtil.setObjectAttributes(project, self.data, {
            'title': None,
            'role_id': {'formName': 'roleId'},
            'skillLevelBit': None,
            'description': None,
            'background': None,
            'instructions': None,
            'employer_id': {'formName': 'employerId'}
        })
        if image := self.data.get('image'):
            project.image = image

        try:
            isChanged = any([
                SkillView.setProjectSkills(project, self.data.get('skills')),
                self.setEvaluationCriteria(project, self.data.get('evaluationCriteria')),
                self.setFiles(project, self.files.get('files', []), self.data.get('filesMetaData', []), request)
            ])
        except ValueError as e:
            return Response(status=status.HTTP_409_CONFLICT, data=e.__str__())

        if isChanged:
            project.modifiedDateTime = timezone.now()

        project.save()
        self.createOrUpdateCustomProject(project)
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

    @atomic
    def createOrUpdateCustomProject(self, project):
        """ Keep custom project in sync with project. These are one for one. Custom project is technically not needed
        but leaving in place for now to allow for more flexibility if needed in the future.
        """
        from upapp.apis.employer import JobPostingView
        customProjects = JobPostingView.getCustomProjects(True)
        customProject = customProjects.get(JobPostingView.generateUniqueCustomProjectKey(project))
        if not customProject:
            customProject = CustomProject(
                project=project,
                skillLevelBit=project.skillLevelBit
            )
            customProject.save()

        # Remove existing skills
        for skill in customProject.skills.all():
            customProject.skills.remove(skill)

        # Update new skills
        for skill in project.skills.all():
            customProject.skills.add(skill)


    @staticmethod
    def getProject(projectId):
        try:
            return Project.objects \
                .select_related('employer', 'role') \
                .prefetch_related('evaluationCriteria', 'projectFile', 'skills') \
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
            .select_related('employer', 'role')\
            .prefetch_related('evaluationCriteria', 'projectFile', 'skills')\
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
                    file=file,
                    modifiedDateTime=timezone.now(),
                    createdDateTime=timezone.now()
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
                })
                if file:
                    existingProjectFile.file = file
                    existingProjectFile.modifiedDateTime = timezone.now()
                existingProjectFile.save()

        deleteProjectFileIds = [id for id in existingProjectFiles.keys() if id not in usedProjectFileIds]
        if deleteProjectFileIds:
            isChanged = True
            ProjectFile.objects.filter(id__in=deleteProjectFileIds).delete()

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
                })
                existingCriterion.save()
                usedCriteriaIds.append(existingCriterion.id)
            else:
                newCriterion = ProjectEvaluationCriterion(
                    project_id=project.id,
                    criterion=criterion['criterion'],
                    category=criterion.get('category'),
                )
                newCriterion.save()
                isChanged = True

        deleteCriteriaIds = [id for id in existingCriteria.keys() if id not in usedCriteriaIds]
        if deleteCriteriaIds:
            isChanged = True
            ProjectEvaluationCriterion.objects.filter(id__in=deleteCriteriaIds).delete()

        return isChanged


class RoleView(UproveAPIView):

    def get(self, request, roleId=None):
        if roleId:
            return Response(status=status.HTTP_200_OK, data=getSerializedRole(self.getRole(roleId)))

        return Response(status=status.HTTP_200_OK, data=[
            getSerializedRole(r) for r in Role.objects.all()
        ])

    def post(self, request):
        if not self.isAdmin:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        role = Role()
        self.updateRole(role)
        return Response(status=status.HTTP_200_OK, data=getSerializedRole(self.getRole(role.id)))

    def put(self, request, roleId=None):
        if not self.isAdmin:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        roleId = roleId or request.data.get('id')
        if not roleId:
            return Response('A project role ID is required', status=status.HTTP_400_BAD_REQUEST)

        role = self.getRole(roleId)
        self.updateRole(role)
        return Response(status=status.HTTP_200_OK, data=getSerializedRole(self.getRole(role.id)))

    def delete(self, request, roleId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        roleId = roleId or request.data.get('id')
        role = self.getRole(roleId)
        role.delete()
        return Response(status=status.HTTP_200_OK, data=roleId)

    @atomic
    def updateRole(self, role):
        role.name = self.data['name']

        # Try saving role. Integrity error indicates role name already exists
        try:
            role.save()
        except IntegrityError as e:
            raise e

    @staticmethod
    def getRole(roleId):
        try:
            return Role.objects.get(id=roleId)
        except Role.DoesNotExist as e:
            raise e


class SkillView(APIView):

    @atomic
    def post(self, request):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            skill = Skill()
            self.saveSkill(request.data, skill)
            return Response(status=status.HTTP_200_OK, data=getSerializedSkill(skill))
        except IntegrityError as e:
            raise e
        except ValueError as e:
            return Response(status=status.HTTP_409_CONFLICT, data=e.__str__())

    @atomic
    def put(self, request, skillId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        skillId = skillId or request.data.get('id')
        if not skillId:
            return Response('A project skill ID is required', status=status.HTTP_400_BAD_REQUEST)

        skill = self.getSkill(skillId)
        try:
            self.saveSkill(request.data, skill)
            return Response(status=status.HTTP_200_OK, data=getSerializedSkill(skill))
        except IntegrityError as e:
            raise e
        except ValueError as e:
            return Response(status=status.HTTP_409_CONFLICT, data=e.__str__())

    def delete(self, request, skillId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        skillId = skillId or request.data.get('id')
        skill = self.getSkill(skillId)
        skill.delete()
        return Response(status=status.HTTP_200_OK, data=skillId)

    @staticmethod
    def getSkill(skillId):
        try:
            return Skill.objects.get(id=skillId)
        except Skill.DoesNotExist as e:
            raise e

    @staticmethod
    def saveSkill(skillData, skill):
        """Update skill data and save it
        :param skillData: Dict of form data
        :param skill: Skill object
        :return: boolean of whether the skill was updated
        """
        isUpdated = dataUtil.setObjectAttributes(skill, skillData, {
            'name': None,
            'instruction': None,
            'skillProject_id': {'formName': 'projectId'},
        })
        skill.save()
        return isUpdated


    @staticmethod
    def updateOrCreateSkill(skillData, allSkillsDict):
        """
        :param skillData: Dict of form data
        :param allSkillsDict: Dict of [skillId]: [skill] entries
        """
        skill = allSkillsDict.get(skillData['id'], Skill())
        SkillView.saveSkill(skillData, skill)
        return skill

    @staticmethod
    def setProjectSkills(project, skillsData):
        """Create/update skills and then associate them with a foreign object
        :param project: Project object
        :param skillsData: A dict of form data
        """
        with atomic():
            isChanged = False
            if project.id:
                oldSkillIds = {s.id for s in project.skills.all()}
                diff = oldSkillIds.symmetric_difference(set([s['id'] for s in skillsData]))
                isChanged = bool(len(diff))
                Skill.objects.filter(id__in=diff, skillProject_id=project.id).delete()
                project.skills.clear()

            existingSkills = {s.id: s for s in Skill.objects.filter(skillProject_id=project.id)}
            for skillData in skillsData:
                skillData['projectId'] = project.id
                skill = SkillView.updateOrCreateSkill(skillData, existingSkills)
                project.skills.add(skill)

            return isChanged

    @staticmethod
    def setSkillIds(customProject, skillIds):
        isChanged = False

        if customProject.id:
            oldSkillIds = {s.id for s in customProject.skills.all()}
            diff = oldSkillIds.symmetric_difference(set(skillIds))
            isChanged = bool(len(diff))
            customProject.skills.clear()

        existingSkills = {s.id: s for s in Skill.objects.filter(skillProject_id=customProject.project_id)}
        requiredSkillIds = {s.id for s in existingSkills.values() if s.isRequired}
        skillIds = set(skillIds).union(requiredSkillIds)
        for skillId in skillIds:
            skill = existingSkills.get(skillId)
            customProject.skills.add(skill)

        return isChanged
