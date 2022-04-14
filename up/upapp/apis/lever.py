import hashlib
import hmac
import os
import requests
from datetime import datetime, timedelta

from django.db.models import Q
from django.db.transaction import atomic
from django.http import HttpResponseRedirect
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp.scraper.scraper.utils.normalize import normalizeJobTitle
from upapp import security
from upapp.apis import UproveAPIView
from upapp.apis.employer import JobPostingView
from upapp.models import Employer, EmployerJob, RoleTitle
from upapp.utils import dataUtil

RECORD_LIMIT = 20000
LEVER_UPROVE_TAG = 'uprove'
LEVER_TIMESTAMP_START = datetime(1970, 1, 1, 0, 0, 0)

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

    data = response.json()

    employer.isLeverOn = True
    employer.leverAccessToken = data['access_token']
    employer.leverRefreshToken = data.get('refresh_token')
    employer.save()

    return HttpResponseRedirect('/employerDashboard/')


class LeverLogOut(UproveAPIView):

    def post(self, request):
        employer = Employer.objects.get(id=self.user.employer_id)
        employer.isLeverOn = False
        return Response(status=status.HTTP_200_OK)


class LeverOpportunities(UproveAPIView):

    def get(self, request, opportunityId=None):
        if not self.user or not self.user.employer_id:
            return Response('You must be logged in', status=status.HTTP_401_UNAUTHORIZED)
        employer = Employer.objects.get(id=self.user.employer_id)
        opportunities = getLeverItems('opportunities', employer, itemId=opportunityId)
        return Response(status=status.HTTP_200_OK, data=opportunities)


class LeverPostings(UproveAPIView):

    @atomic
    def post(self, request):
        if not self.user or not self.user.employer_id:
            return Response('You must be logged in', status=status.HTTP_401_UNAUTHORIZED)
        employer = Employer.objects.get(id=self.user.employer_id)
        postings = getLeverItems('postings', employer)
        currentLeverJobs = {
            j.leverPostingKey: j for j in
            JobPostingView.getEmployerJobs(employerId=self.user.employer_id, jobFilter=Q(leverPostingKey__isnull=False))
        }
        roleTitles = {r.roleTitle: r for r in RoleTitle.objects.all()}

        processedLeverKeys = []
        for posting in postings:
            if LEVER_UPROVE_TAG not in posting['tags']:
                continue

            leverPostingKey = posting['id']
            processedLeverKeys.append(leverPostingKey)

            if not (currentJob := currentLeverJobs.get(leverPostingKey)):
                currentJob = EmployerJob(
                    employer=employer,
                    createdDateTime=timezone.now(),
                    modifiedDateTime=timezone.now(),
                    leverPostingKey=leverPostingKey
                )
                currentLeverJobs[leverPostingKey] = currentJob
            isUpdated = dataUtil.setObjectAttributes(currentJob, posting, {
                'jobTitle': {'formName': 'text'},
            })
            currentJob.role = normalizeJobTitle(currentJob.jobTitle, roleTitles)

            jobLists = []
            for jobList in posting['content']['lists']:
                jobLists.append(f'<h5>{jobList["text"]}</h5>')
                jobLists.append(f'<ul>{jobList["content"]}</ul>')
            jobDescription = posting['content']['descriptionHtml'] + ''.join(jobLists) + posting['content']['closingHtml']
            isUpdated = updateAndGetIsChanged(currentJob, 'jobDescription', jobDescription) or isUpdated

            state = posting['state']
            isConfidential = posting['confidentiality'] == 'confidential'
            isUpdated = updateAndGetIsChanged(currentJob, 'isInternal', state == 'internal' or isConfidential) or isUpdated

            closeDate = None
            if state in ('closed', 'rejected'):
                closeDate = currentJob.closeDate or getLeverDateTime(posting['updatedAt']).date()
            isUpdated = updateAndGetIsChanged(currentJob, 'closeDate', closeDate) or isUpdated

            openDate = currentJob.openDate or getLeverDateTime(posting['createdAt']).date()
            if state in ('draft', 'pending'):
                openDate = None
            isUpdated = updateAndGetIsChanged(currentJob, 'openDate', openDate) or isUpdated

            if isUpdated:
                currentJob.modifiedDateTime = timezone.now()
            currentJob.save()

        # Close any jobs that are no longer in the Lever feed
        for leverKey, job in currentLeverJobs.items():
            if leverKey in processedLeverKeys or job.closeDate:
                continue
            job.closeDate = timezone.now().date()
            job.modifiedDateTime = timezone.now()
            job.save()

        return Response(status=status.HTTP_200_OK)


class LeverStages(UproveAPIView):

    def get(self, request, stageId=None):
        relativeUrl = f'stages/{stageId}' if stageId else 'stages'
        employer = Employer.objects.get(id=self.user.employer_id)
        response = getLeverRequestWithRefresh(employer, relativeUrl)
        return Response(status=status.HTTP_200_OK, data=response.get('data', []))


class LeverConfig(UproveAPIView):

    def put(self, request, employerId=None):
        if not employerId:
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        if not security.isPermittedEmployer(request, employerId):
            return Response('You are not permitted to make this change', status=status.HTTP_401_UNAUTHORIZED)

        employer = Employer.objects.get(id=employerId)

        isChanged = dataUtil.setObjectAttributes(employer, self.data, {
            'leverTriggerStageKey': {'isIgnoreExcluded': True},
            'leverCompleteStageKey': {'isIgnoreExcluded': True},
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

    def validateRequest(self, request, hookAttr, employerId=None):
        data = request.data
        if not employerId:
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        employer = Employer.objects.get(id=employerId)
        hookKey = getattr(employer, hookAttr)
        if not hookKey:
            return Response('The signature token for this webhook has not been configured', status=status.HTTP_400_BAD_REQUEST)

        isAuthorizedRequest = validateLeverRequest(data, hookKey)
        if not isAuthorizedRequest:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return data


class LeverChangeStage(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, 'leverHookStageChangeToken', employerId=employerId)
        if isinstance(data, Response):
            return data

        # TODO: Parse the data
        # fromStageId
        # toStageId
        # contactId
        # opportunityId

        return Response(status=status.HTTP_200_OK)


class LeverArchive(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, 'leverHookArchive', employerId=employerId)
        if isinstance(data, Response):
            return data

        # TODO: Parse the data

        return Response(status=status.HTTP_200_OK)


class LeverHired(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, 'leverHookHired', employerId=employerId)
        if isinstance(data, Response):
            return data

        # TODO: Parse the data

        return Response(status=status.HTTP_200_OK)


class LeverDeleted(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, 'leverHookDeleted', employerId=employerId)
        if isinstance(data, Response):
            return data

        # TODO: Parse the data

        return Response(status=status.HTTP_200_OK)


def getLeverItems(url, employer, itemId=None):
    hasNext = True
    next = None
    data = []
    relativeUrl = f'{url}/{itemId}' if itemId else url
    while hasNext and len(data) < RECORD_LIMIT:
        response = getLeverRequestWithRefresh(employer, relativeUrl, nextKey=next)
        hasNext = response.get('hasNext')
        next = response.get('next')
        data += response.get('data', [])

    return data


def getLeverRequestWithRefresh(employer, relativeUrl, nextKey=None):
    body = {'responseType': 'json'}
    if nextKey:
        body['offset'] = nextKey
    url = f'{os.getenv("LEVER_BASE_URL")}{relativeUrl}'
    response = requests.get(url, body, headers={'Authorization': f'Bearer {employer.leverAccessToken}'})

    # Update the access tokens if they have expired
    if response.status_code != 200:
        response = requests.post(os.getenv('LEVER_AUTH_TOKEN_URL'), {
            'client_id': os.getenv('LEVER_CLIENT_ID'),
            'client_secret': os.getenv('LEVER_CLIENT_SECRET'),
            'grant_type': 'refresh_token',
            'refresh_token': employer.leverRefreshToken
        })

        if response.status_code != 200:
            raise ConnectionError()

        data = response.json()
        employer.leverAccessToken = data['access_token']
        employer.leverRefreshToken = data.get('refresh_token')
        employer.save()
        response = requests.get(url, body, headers={'Authorization': f'Bearer {employer.leverAccessToken}'})

    return response.json()


def getLeverDateTime(timestamp):
    return LEVER_TIMESTAMP_START + timedelta(milliseconds=timestamp)


def updateAndGetIsChanged(obj, attr, newVal):
    currentVal = getattr(obj, attr)
    setattr(obj, attr, newVal)
    return currentVal != getattr(obj, attr)


def validateLeverRequest(requestData, signatureToken):
    plainText = requestData.get('token') + str(requestData['triggeredAt'])
    hash = hmac.new(bytes(signatureToken, 'UTF-8'), plainText.encode(), hashlib.sha256).hexdigest()
    return hash == requestData['signature']
