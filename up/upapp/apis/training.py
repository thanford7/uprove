from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from upapp import security
from upapp.apis import UproveAPIView
from upapp.modelSerializers import getSerializedTrainingCourse
from upapp.models import TrainingCourse
from upapp.utils import dataUtil


class TrainingCourseView(UproveAPIView):

    def get(self, request, courseId=None):
        courseId = courseId or self.data.get('id')
        if courseId:
            data = getSerializedTrainingCourse(self.getCourses(courseId=courseId))
        elif searchText := self.data.get('search'):
            searchText = searchText[0]
            courseFilter = Q(title__iregex=f'^.*{searchText}.*$')
            data = [getSerializedTrainingCourse(c) for c in self.getCourses(filter=courseFilter)]
        else:
            data = [getSerializedTrainingCourse(c) for c in self.getCourses()]

        return Response(
            status=status.HTTP_200_OK,
            data=data
        )

    def post(self, request):
        if not security.isPermittedAdmin(user=self.user):
            return Response('You are not authorized to post course content', status=status.HTTP_401_UNAUTHORIZED)

        course = TrainingCourse()
        self.updateCourse(course, self.data)
        course.save()
        return Response(status=status.HTTP_200_OK, data=getSerializedTrainingCourse(course))

    def put(self, request, courseId=None):
        if not security.isPermittedAdmin(user=self.user):
            return Response('You are not authorized to post course content', status=status.HTTP_401_UNAUTHORIZED)

        courseId = courseId or self.data.get('id')

        if not courseId:
            return Response('A course ID is required', status=status.HTTP_400_BAD_REQUEST)

        course = self.getCourses(courseId=courseId)
        self.updateCourse(course, self.data)
        course.save()
        return Response(status=status.HTTP_200_OK, data=getSerializedTrainingCourse(course))

    def delete(self, request, courseId=None):
        if not security.isPermittedAdmin(user=self.user):
            return Response('You are not authorized to post course content', status=status.HTTP_401_UNAUTHORIZED)

        courseId = courseId or self.data.get('id')

        if not courseId:
            return Response('A course ID is required', status=status.HTTP_400_BAD_REQUEST)

        course = self.getCourses(courseId=courseId)
        course.delete()
        return Response(status=status.HTTP_200_OK, data=courseId)

    @staticmethod
    def getCourses(courseId=None, teachableCourseId=None, filter=None):
        filter = filter or Q()
        if courseId:
            filter &= Q(id=courseId)

        if teachableCourseId:
            filter &= Q(teachableCourseId=teachableCourseId)

        courses = TrainingCourse.objects.filter(filter)
        if courseId or teachableCourseId:
            if not courses:
                raise TrainingCourse.DoesNotExist
            return courses[0]

        return courses

    @staticmethod
    def updateCourse(course, data):
        dataUtil.setObjectAttributes(course, data, {
            'title': None,
            'shortDescription': None,
            'coverImage': None,
            'urlSalesPage': None,
            'urlCoursePage': None,
            'teachableCourseId': None,
            'priceBasic': None,
        })
