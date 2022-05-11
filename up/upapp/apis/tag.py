from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from upapp.apis import UproveAPIView
from upapp.models import Tag
from upapp.modelSerializers import getSerializedTag
from upapp.utils import dataUtil


class TagView(UproveAPIView):

    def get(self, request):
        if tagId := self.data.get('id'):
            return Response(status=status.HTTP_200_OK, data=getSerializedTag(self.getTag(tagId)))
        if search := self.data.get('search'):
            q = Q(title__iregex=f'^.*{search}.*$') & Q(type__in=self.data.get('tagType'))
            tags = Tag.objects.filter(q)
            return Response(status=status.HTTP_200_OK, data=[getSerializedTag(t) for t in tags])

    @staticmethod
    def getTag(tagId):
        return Tag.objects.get(id=tagId)

    @staticmethod
    def updateOrCreate(tagData, tag=None):
        if not tag:
            try:
                tag = Tag.objects.get(title=tagData.get('title'), type=tagData.get('type'))
            except Tag.DoesNotExist:
                tag = Tag()
        # Note: Tag description can only be set from the admin menu to avoid different users overwriting
        # the default description
        dataUtil.setObjectAttributes(tag, tagData, {
            'title': None,
            'type': None
        })
        tag.save()
        return tag
