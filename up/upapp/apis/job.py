from django.db.transaction import atomic
from rest_framework import authentication, status
from rest_framework.response import Response

from upapp.apis import UproveAPIView
from upapp.models import JobTemplate
from upapp.modelSerializers import getSerializedJobTemplate
import upapp.security as security
from upapp.utils import dataUtil


class JobTemplateView(UproveAPIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def get(self, request, templateId=None):
        templateId = templateId or self.data.get('id')
        if templateId:
            return Response(status=status.HTTP_200_OK, data=getSerializedJobTemplate(self.getJobTemplates(templateId)))

        return Response(status=status.HTTP_200_OK, data=[getSerializedJobTemplate(t) for t in self.getJobTemplates()])

    @atomic
    def post(self, request):
        if not security.isPermittedAdmin(request):
            return Response('You are not permitted to create a job template', status=status.HTTP_401_UNAUTHORIZED)
        template = JobTemplate(
            title=self.data['title'],
            description=self.data['description']
        )
        template.save()
        return Response(status=status.HTTP_200_OK, data=getSerializedJobTemplate(template))

    @atomic
    def put(self, request, templateId=None):
        templateId = templateId or self.data.get('id')
        if not templateId:
            return Response('A template ID is required', status=status.HTTP_400_BAD_REQUEST)

        template = self.getJobTemplates(templateId=templateId)
        dataUtil.setObjectAttributes(template, request.data, {
            'title': None,
            'description': None
        })
        template.save()
        return Response(status=status.HTTP_200_OK, data=getSerializedJobTemplate(template))

    @atomic
    def delete(self, request, templateId=None):
        templateId = templateId or self.data.get('id')
        if not templateId:
            return Response('A template ID is required', status=status.HTTP_400_BAD_REQUEST)

        template = self.getJobTemplates(templateId=templateId)
        template.delete()
        return Response(status=status.HTTP_200_OK, data=templateId)

    @staticmethod
    def getJobTemplates(templateId=None):
        if templateId:
            return JobTemplate.objects.get(id=templateId)
        return JobTemplate.objects.all()
