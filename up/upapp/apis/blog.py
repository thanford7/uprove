from datetime import date, datetime

from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp.models import BlogPost, BlogTag
from upapp.modelSerializers import getSerializedBlog
import upapp.security as security
from upapp.utils import dataUtil, dateUtil


class BlogPostView(APIView):

    def get(self, request, blogId=None):
        if blogId:
            data = self.getBlogPost(blogId)
        else:
            data = [getSerializedBlog(b) for b in self.getBlogPosts()]
        return Response(status=status.HTTP_200_OK, data=data)

    @atomic
    def post(self, request):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        blogPost = BlogPost(
            title=data['title'],
            author_id=data['authorId'],
            picture=data.get('picture'),
            post=data['post'],
            publishDate=dateUtil.deserializeDateTime(data.get('publishDate'), dateUtil.FormatType.DATE, allowNone=True),
            modifiedDateTime=datetime.utcnow(),
            createdDateTime=datetime.utcnow(),
        )
        blogPost.save()
        if blogTagData := data.get('blogTags'):
            self.addBlogTags(blogPost, blogTagData)

        return Response(status=status.HTTP_200_OK, data=getSerializedBlog(self.getBlogPost(blogPost.id)))

    @atomic
    def put(self, request, blogId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        blogId = blogId or data['id']
        if not blogId:
            return Response('A blog ID is required', status=status.HTTP_400_BAD_REQUEST)

        blogPost = self.getBlogPost(blogId)
        dateGetter = lambda val: dateUtil.deserializeDateTime(val, dateUtil.FormatType.DATE, allowNone=True)
        dataUtil.setObjectAttributes(blogPost, data, {
            'title': None,
            'author_id': {'formName': 'authorId'},
            'post': None,
            'publishDate': {'propFunc': dateGetter}
        })

        if picture := data.get('picture'):
            blogPost.picture = picture
        blogPost.save()

        if blogTagData := data.get('blogTags'):
            self.addBlogTags(blogPost, blogTagData)

        return Response(status=status.HTTP_200_OK, data=getSerializedBlog(self.getBlogPost(blogPost.id)))

    @atomic
    def delete(self, request, blogId=None):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        blogId = blogId or data['id']
        if not blogId:
            return Response('A blog ID is required', status=status.HTTP_400_BAD_REQUEST)

        blogPost = self.getBlogPost(blogId)
        blogPost.delete()
        return Response(status=status.HTTP_200_OK, data=blogId)

    @staticmethod
    def addBlogTags(blogPost, blogTagData):
        existingBlogTags = {b.name: b for b in BlogPostView.getBlogTags()}
        blogPost.blogTags.clear()
        for blogTagName in blogTagData:
            blogTagName = dataUtil.capitalizeAllWords(blogTagName)
            if not (blogTag := existingBlogTags.get(blogTagName)):
                blogTag = BlogTag(name=blogTagName)
                blogTag.save()
            blogPost.blogTags.add(blogTag)

    @staticmethod
    def getBlogPost(blogId):
        try:
            return BlogPost.objects.select_related('author').prefetch_related('blogTags').get(id=blogId)
        except BlogPost.DoesNotExist as e:
            raise e

    @staticmethod
    def getBlogPosts(isPublishedOnly=True):
        blogPosts = BlogPost.objects.select_related('author').prefetch_related('blogTags').all()
        if isPublishedOnly:
            blogPosts = blogPosts.filter(publishDate__lte=date.today())
        return blogPosts

    @staticmethod
    def getBlogTags():
        return BlogTag.objects.all()
