from django.db.models import Q
from rest_framework import authentication, status
from rest_framework.response import Response
from rest_framework.views import APIView

from modelSerializers import getSerializedProject
from upapp.models import Project


class ProjectView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def get(self, request, projectId=None):
        if projectId:
            return Response(getSerializedProject(self.getProject(projectId)), status=status.HTTP_200_OK)

        employerId = request.data.get('employerId')
        return Response([getSerializedProject(p) for p in self.getProjects(employerId=employerId)])

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
