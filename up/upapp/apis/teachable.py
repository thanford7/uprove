from django.db.transaction import atomic
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp.apis.training import TrainingCourseView
from upapp.models import UserTraining, User, TrainingCourse, TeachableUser


class BaseTeachableChange(APIView):
    parser_classes = [JSONParser]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.data = request.data[0]['object']

        try:
            self.course = TrainingCourseView.getCourses(teachableCourseId=self.data['course']['id'])
        except TrainingCourse.DoesNotExist as e:
            raise e

        self.teachableUser = self.getOrCreateTeachableUser(self.data['user'])

    @staticmethod
    @atomic
    def getOrCreateTeachableUser(userData):
        userEmail = userData['email']
        try:
            teachableUser = TeachableUser.objects.get(email=userEmail)
        except TeachableUser.DoesNotExist:
            try:
                uproveUser = User.objects.get(email=userEmail)
            except User.DoesNotExist:
                uproveUser = None

            teachableUser = TeachableUser(
                user=uproveUser,
                email=userEmail,
                name=userData['name'],
                teachableUserId=userData['id'],
                createdDateTime=timezone.now()
            )

            teachableUser.save()

        return teachableUser


class TeachableEnrolled(BaseTeachableChange):

    @atomic
    def post(self, request):
        # Protect against duplicate course issue
        try:
            UserTraining.objects.get(teachableUser=self.teachableUser, course=self.course)
        except UserTraining.DoesNotExist:
            userTraining = UserTraining(
                teachableUser=self.teachableUser,
                course=self.course,
                enrolledDateTime=timezone.now()
            )
            userTraining.save()

        return Response(status=status.HTTP_200_OK)


class TeachableCourseProgress(BaseTeachableChange):

    @atomic
    def post(self, request):
        try:
            userTraining = UserTraining.objects.get(teachableUser=self.teachableUser, course=self.course)
        except UserTraining.DoesNotExist as e:
            raise e

        userTraining.completionPct = self.data['percent_complete']
        if userTraining.completionPct == 100:
            userTraining.completedDateTime = timezone.now()

        userTraining.save()

        return Response(status=status.HTTP_200_OK)
