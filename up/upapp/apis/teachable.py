from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp.apis.training import TrainingCourseView
from upapp.models import UserTraining, User, TrainingCourse


class BaseTeachableChange(APIView):
    parser_classes = [JSONParser]


class TeachableEnrolled(BaseTeachableChange):

    def post(self, request):
        data = request.data

        try:
            course = TrainingCourseView.getCourses(teachableCourseId=data['course']['id'])
        except TrainingCourse.DoesNotExist as e:
            raise e

        try:
            user = User.objects.get(data['user']['email'])
        except User.DoesNotExist as e:
            raise e

        userTraining = UserTraining(
            user=user,
            course=course,
            enrolledDateTime=timezone.now()
        )

        userTraining.save()
        return Response(status=status.HTTP_200_OK)