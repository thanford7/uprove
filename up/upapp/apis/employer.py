from datetime import datetime

from django.db.transaction import atomic
from psycopg2 import IntegrityError
from rest_framework import authentication, status
from rest_framework.response import Response
from rest_framework.views import APIView

import upapp.security as security
from upapp.modelSerializers import getSerializedEmployer
from upapp.models import Employer
from upapp.utils import dataUtil


class EmployerView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def get(self, request, employerId=None):
        if employerId:
            data = getSerializedEmployer(self.getEmployer(employerId))
        else:
            data = [getSerializedEmployer(e) for e in self.getEmployers()]
        return Response(status=status.HTTP_200_OK, data=data)

    @atomic
    def post(self, request):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        try:
            employer = Employer(
                companyName=data['companyName'],
                logo=data.get('logo'),
                modifiedDateTime=datetime.utcnow(),
                createdDateTime=datetime.utcnow()
            )
            employer.save()
            return Response(status=status.HTTP_200_OK, data=getSerializedEmployer(employer))
        except IntegrityError:
            return Response(f'Company with name={data["companyName"]} already exists.', status=status.HTTP_409_CONFLICT)

    def put(self, request, employerId=None):
        employerId = employerId or request.data.get('id')
        if not employerId:
            return Response('Employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        if not any((security.isPermittedAdmin(request), security.isPermittedEmployer(request, employerId))):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        employer = self.getEmployer(employerId)
        data = request.data
        try:
            dataUtil.setObjectAttributes(employer, request.data, {
                'companyName': None,
                'logo': None
            })
            employer.save()
            return Response(status=status.HTTP_200_OK, data=getSerializedEmployer(employer))
        except IntegrityError:
            return Response(f'Company with name={data["companyName"]} already exists.', status=status.HTTP_409_CONFLICT)

    def delete(self, request, employerId=None):
        employerId = employerId or request.data.get('id')
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not employerId:
            return Response('Employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        self.getEmployer(employerId).delete()
        return Response(status=status.HTTP_200_OK, data=employerId)

    @staticmethod
    def getEmployer(employerId):
        try:
            return Employer.objects.get(id=employerId)
        except Employer.DoesNotExist as e:
            raise e

    @staticmethod
    def getEmployers():
        return Employer.objects.all()