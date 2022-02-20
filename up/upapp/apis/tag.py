from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from upapp.apis import UproveAPIView
from upapp.models import Tag
from upapp.modelSerializers import getSerializedTag


class TagView(UproveAPIView):

    def get(self, request):
        if tagId := self.data.get('id'):
            return Response(status=status.HTTP_200_OK, data=getSerializedTag(self.getTag(tagId)))
        if search := self.data.get('search'):
            q = Q(title__iregex=f'^.*{search}.*$') & Q(type=self.data.get('tagType'))
            tags = Tag.objects.filter(q)
            return Response(status=status.HTTP_200_OK, data=[getSerializedTag(t) for t in tags])

    def post(self, request):
        pass

    def put(self, request):
        pass

    @staticmethod
    def getTag(tagId):
        return Tag.objects.get(id=tagId)

    @staticmethod
    def getOrCreate(data):
        pass
