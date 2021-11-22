from datetime import datetime

from django.db import IntegrityError
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp import security
from upapp.modelSerializers import getSerializedProject, getSerializedProjectFunction, getSerializedProjectSkill
from upapp.models import Project, ProjectFunction, ProjectSkill, ProjectFile
from upapp.utils import dataUtil


class ProjectView(APIView):

    def get(self, request, projectId=None):
        projectId = projectId or request.data['id']
        if projectId:
            return Response(getSerializedProject(self.getProject(projectId)), status=status.HTTP_200_OK)

        employerId = request.data.get('employerId')
        return Response([getSerializedProject(p) for p in self.getProjects(employerId=employerId)])

    def post(self, request):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        project = Project(
            title=data.title,
            function=FunctionView.getProjectFunction(data['functionId']),
            skillLevelBits=data['skillLevelBits'],
            description=data['description'],
            employer_id=data.get('employer'),
            modifiedDateTime=datetime.utcnow(),
            createdDateTime=datetime.utcnow()
        )
        for skill in ProjectSkill.objects.filter(id__in=data['skillIds']):
            project.skills.add(skill)

        for file in data.get('files', []):
            file = ProjectFile(

            )

    def put(self, request, projectId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        projectId = projectId or request.data['id']
        if not projectId:
            return Response('A project ID is required', status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, projectId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        projectId = projectId or request.data['id']
        if not projectId:
            return Response('A project ID is required', status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def getProject(projectId):
        try:
            return Project.objects \
                .select_related('employer', 'function') \
                .prefetch_related('projectFile', 'skills') \
                .get(id=projectId)
        except Project.DoesNotExist as e:
            raise e

    @staticmethod
    def getProjects(employerId=None):
        q = Q(employer_id__isnull=True)
        if employerId:
            q |= Q(employer_id=employerId)
        return Project.objects\
            .select_related('employer', 'function')\
            .prefetch_related('projectFile', 'skills')\
            .filter(q)


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
        return Response(status=status.HTTP_200_OK)

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
            projectSkill = ProjectSkill(skillName=request.data['skillName'])
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
            projectSkill.skillName = request.data['skillName']
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
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def getProjectSkill(skillId):
        try:
            return ProjectSkill.objects.get(id=skillId)
        except ProjectSkill.DoesNotExist as e:
            raise e
