from rest_framework import authentication
from rest_framework.views import APIView

from upapp.models import Employer


class EmployerView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def get(self, request, employerId=None):
        pass

    @staticmethod
    def getEmployer(employerId):
        try:
            return Employer.objects.get(id=employerId)
        except Employer.DoesNotExist as e:
            raise e

    @staticmethod
    def getEmployers():
        return Employer.objects.all()