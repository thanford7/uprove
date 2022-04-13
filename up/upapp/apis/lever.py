import hashlib
import hmac
import os
import requests

from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp import security
from upapp.apis import UproveAPIView
from upapp.models import Employer
from upapp.utils import dataUtil

RECORD_LIMIT = 20000


def leverIntegrate(request):
    if request.GET.get('state') != os.getenv('LEVER_STATE'):
        raise ConnectionError()

    user = security.getSessionUser(request)
    employer = Employer.objects.get(id=user.employer_id)
    response = requests.post(os.getenv('LEVER_AUTH_TOKEN_URL'), {
        'client_id': os.getenv('LEVER_CLIENT_ID'),
        'client_secret': os.getenv('LEVER_CLIENT_SECRET'),
        'grant_type': 'authorization_code',
        'code': request.GET.get('code'),
        'redirect_uri': request.build_absolute_uri('/integrate/')
    })

    if response.status_code != 200:
        raise ConnectionError()

    employer.isLeverOn = True
    employer.save()

    data = response.json()
    request.session['leverAccessToken'] = data['access_token']
    request.session['leverRefreshToken'] = data.get('refresh_token')

    return HttpResponseRedirect('/employerDashboard/')


class LeverLogOut(UproveAPIView):

    def post(self, request):
        employer = Employer.objects.get(id=self.user.employer_id)
        employer.isLeverOn = False
        return Response(status=status.HTTP_200_OK)


class LeverOpportunities(APIView):

    def get(self, request):
        hasNext = True
        next = None
        data = []
        while hasNext and len(data) < RECORD_LIMIT:
            response = getLeverRequestWithRefresh(
                request,
                f'{os.getenv("LEVER_BASE_URL")}opportunities',
                {'responseType': 'json', 'offset': next},
                headers={'Authorization': f'Bearer {request.session.get("leverAccessToken")}'},
            ).json()
            hasNext = response.get('hasNext')
            next = response.get('next')
            data += response.get('data', [])

        return Response(status=status.HTTP_200_OK, data=data)


class LeverConfig(UproveAPIView):

    def put(self, request, employerId=None):
        if not employerId:
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        if not security.isPermittedEmployer(request, employerId):
            return Response('You are not permitted to make this change', status=status.HTTP_401_UNAUTHORIZED)

        employer = Employer.objects.get(id=employerId)

        isChanged = dataUtil.setObjectAttributes(employer, self.data, {
            'leverHookStageChangeToken': {'isIgnoreExcluded': True},
            'leverHookArchive': {'isIgnoreExcluded': True},
            'leverHookHired': {'isIgnoreExcluded': True},
            'leverHookDeleted': {'isIgnoreExcluded': True},
        })
        if isChanged:
            employer.save()

        return Response(status=status.HTTP_200_OK)


class BaseLeverChange(APIView):
    parser_classes = [JSONParser]

    def validateRequest(self, request, employerId=None):
        data = request.data
        if (not employerId) or (not security.isPermittedEmployer(request, employerId)):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        employer = Employer.objects.get(id=employerId)
        isAuthorizedRequest = validateLeverRequest(data, employer.leverHookArchive)
        if not isAuthorizedRequest or not employerId or not security.isPermittedEmployer(request, employerId):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return data


class LeverChangeStage(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, employerId=employerId)
        if isinstance(data, Response):
            return data

        # TODO: Parse the data

        return Response(status=status.HTTP_200_OK)


class LeverArchive(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, employerId=employerId)
        if isinstance(data, Response):
            return data

        # TODO: Parse the data

        return Response(status=status.HTTP_200_OK)


class LeverHired(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, employerId=employerId)
        if isinstance(data, Response):
            return data

        # TODO: Parse the data

        return Response(status=status.HTTP_200_OK)


class LeverDeleted(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, employerId=employerId)
        if isinstance(data, Response):
            return data

        # TODO: Parse the data

        return Response(status=status.HTTP_200_OK)


def getLeverRequestWithRefresh(request, url, body, **kwargs):
    response = requests.get(url, body, **kwargs)

    # Update the access tokens if they have expired
    if response.status_code != 200:
        response = requests.post(os.getenv('LEVER_AUTH_TOKEN_URL'), {
            'client_id': os.getenv('LEVER_CLIENT_ID'),
            'client_secret': os.getenv('LEVER_CLIENT_SECRET'),
            'grant_type': 'refresh_token',
            'refresh_token': request.session.get('leverRefreshToken')
        })

        if response.status_code != 200:
            raise ConnectionError()

        data = response.json()
        request.session['leverAccessToken'] = data['access_token']
        request.session['leverRefreshToken'] = data.get('refresh_token')
        response = requests.get(url, body, **kwargs)

    return response


def validateLeverRequest(requestData, signatureToken):
    plainText = requestData.get('token') + str(requestData['triggeredAt'])
    hash = hmac.new(bytes(signatureToken, 'UTF-8'), plainText.encode(), hashlib.sha256).hexdigest()
    return hash == requestData['signature']
