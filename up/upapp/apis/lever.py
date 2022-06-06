import hashlib
import hmac

import requests
from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Q
from django.db.transaction import atomic
from django.http import HttpResponseRedirect
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp import security
from upapp.apis import UproveAPIView
from upapp.models import Employer, EmployerJob, RoleLevel, UserJobApplication
from upapp.scraper.scraper.utils.normalize import normalizeJobTitle
from upapp.utils import dataUtil

RECORD_LIMIT = 20000
LEVER_UPROVE_TAG = 'uprove'
LEVER_TIMESTAMP_START = datetime(1970, 1, 1, 0, 0, 0)
LEVER_WEBHOOK_STAGE_CHANGE = 'stage-change'
LEVER_WEBHOOK_ARCHIVE = 'archive'
LEVER_WEBHOOK_HIRE = 'hire'
LEVER_WEBHOOK_DELETE = 'delete'


def leverIntegrate(request):
    from upapp.urls import apiPath  # Avoid circular import

    if request.GET.get('state') != settings.LEVER_STATE:
        raise ConnectionError('State does not match')

    # Begin oAuth
    user = security.getSessionUser(request)
    employer = Employer.objects.get(id=user.employer_id)
    redirectUrl = request.build_absolute_uri('/integrate/')
    if 'http' in redirectUrl and ('https' not in redirectUrl) and not settings.LEVER_DEBUG:
        redirectUrl = redirectUrl.replace('http', 'https')

    response = requests.post(settings.LEVER_AUTH_TOKEN_URL, {
        'client_id': settings.LEVER_CLIENT_ID,
        'client_secret': settings.LEVER_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': request.GET.get('code'),
        'redirect_uri': redirectUrl
    })

    if response.status_code != 200:
        raise ConnectionError()

    data = response.json()

    employer.isLeverOn = True
    employer.leverAccessToken = data['access_token']
    employer.leverRefreshToken = data.get('refresh_token')
    # End oAuth

    # Begin webhooks
    response = getLeverRequestWithRefresh(
        employer,
        'webhooks/',
    )
    currentWebhooks = response.get('data')
    if currentWebhooks is None:
        raise ConnectionError('Unable to get existing webhooks')

    currentWebhooks = {w['url']: w for w in currentWebhooks}

    if localUrl := settings.LEVER_LOCAL_URL_OVERRIDE:
        baseWebhookUrl = f'https://{localUrl}/{apiPath}lever/change/'
    else:
        baseWebhookUrl = request.build_absolute_uri(f'/{apiPath}lever/change/')
    if 'https' not in baseWebhookUrl:
        baseWebhookUrl = baseWebhookUrl.replace('http', 'https')

    baseConfig = {
        'conditions': {
            'origins': [
                'applied',
                'sourced',
                'referred',
                'university',
                'agency',
                'internal'
            ]
        },
    }

    stageChangeUrl = f'{baseWebhookUrl}{LEVER_WEBHOOK_STAGE_CHANGE}/{employer.id}/'
    if stageChangeUrl not in currentWebhooks:
        response = getLeverRequestWithRefresh(
            employer,
            'webhooks/',
            bodyCfg={
                'url': stageChangeUrl,
                'event': 'candidateStageChange',
                'configuration': baseConfig
            },
            isJSON=True,
            method='POST'
        )
        if not (webhookData := response.get('data')):
            raise ConnectionError('Unable to establish webhook for candidate stage change phase')
        employer.leverHookStageChangeToken = webhookData['configuration']['signatureToken']

    hireUrl = f'{baseWebhookUrl}{LEVER_WEBHOOK_HIRE}/{employer.id}/'
    if hireUrl not in currentWebhooks:
        response = getLeverRequestWithRefresh(
            employer,
            'webhooks/',
            bodyCfg={
                'url': hireUrl,
                'event': 'candidateHired',
                'configuration': baseConfig
            },
            isJSON=True,
            method='POST'
        )
        if not (webhookData := response.get('data')):
            raise ConnectionError('Unable to establish webhook for candidate hired phase')
        employer.leverHookHired = webhookData['configuration']['signatureToken']

    archiveUrl = f'{baseWebhookUrl}{LEVER_WEBHOOK_ARCHIVE}/{employer.id}/'
    if archiveUrl not in currentWebhooks:
        response = getLeverRequestWithRefresh(
            employer,
            'webhooks/',
            bodyCfg={
                'url': archiveUrl,
                'event': 'candidateArchiveChange',
                'configuration': baseConfig
            },
            isJSON=True,
            method='POST'
        )
        if not (webhookData := response.get('data')):
            raise ConnectionError('Unable to establish webhook for candidate archived phase')
        employer.leverHookArchive = webhookData['configuration']['signatureToken']

    deleteUrl = f'{baseWebhookUrl}{LEVER_WEBHOOK_DELETE}/{employer.id}/'
    if deleteUrl not in currentWebhooks:
        response = getLeverRequestWithRefresh(
            employer,
            'webhooks/',
            bodyCfg={
                'url': deleteUrl,
                'event': 'candidateDeleted',
            },
            isJSON=True,
            method='POST'
        )
        if not (webhookData := response.get('data')):
            raise ConnectionError('Unable to establish webhook for candidate deleted phase')
        employer.leverHookDeleted = webhookData['configuration']['signatureToken']
    # End webhooks

    employer.save()

    return HttpResponseRedirect('/employerDashboard/?tab=integrations')


class BaseLeverAPIView(UproveAPIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if not self.user or not self.user.employer_id:
            return Response('You must be logged in', status=status.HTTP_401_UNAUTHORIZED)
        if not kwargs['employerId']:
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        self.employer = Employer.objects.get(id=kwargs['employerId'])

        if (not security.isPermittedEmployer(request, self.employer.id)) or self.isAdmin:
            return Response('You do not have permission to make updates for this employer',
                            status=status.HTTP_401_UNAUTHORIZED)


class LeverLogOut(BaseLeverAPIView):

    def post(self, request, employerId=None):
        self.employer.isLeverOn = False
        self.employer.save()
        return Response(status=status.HTTP_200_OK)


class LeverOpportunities(BaseLeverAPIView):
    CONNECTION_ERROR_MSG = 'Error saving candidate opportunity to Lever: Connection refused. Try clicking the "On" button in the integrations tab on your employer dashboard.'

    def get(self, request, opportunityId=None, employerId=None):
        opportunities = getLeverItems('opportunities', self.employer, itemId=opportunityId)
        return Response(status=status.HTTP_200_OK, data=opportunities)

    @staticmethod
    @atomic
    def addLeverOpportunity(request, user, jobApplication, note=None):
        if jobApplication.leverOpportunityKey:
            return None

        if not jobApplication.employerJob.leverPostingKey:
            return 'Unable to save opportunity to Lever. This job is not linked with an existing posting in Lever.'

        applicant = jobApplication.user
        employer = jobApplication.employerJob.employer
        try:
            resp = getLeverRequestWithRefresh(
                employer,
                f'opportunities?perform_as={user.leverUserKey}',
                bodyCfg={
                    'name': f'{applicant.firstName} {applicant.lastName}',
                    'emails': [applicant.email],
                    'links': [request.build_absolute_uri(f'/profile/{applicant.primaryProfile.id}')] if applicant.primaryProfile else [],
                    'tags': ['uprove'],
                    'sources': ['Uprove'],
                    'origin': 'agency',
                    'postings': [jobApplication.employerJob.leverPostingKey]
                },
                isJSON=True,
                method='POST'
            )
            opportunity = resp.get('data')
            if not opportunity:
                errorMsg = resp.get('message')
                return f'Error saving candidate opportunity to Lever: {errorMsg}'
        except ConnectionError:
            return LeverOpportunities.CONNECTION_ERROR_MSG

        jobApplication.leverOpportunityKey = opportunity['id']
        jobApplication.save()

        if note:
            try:
                resp = getLeverRequestWithRefresh(
                    employer,
                    f'opportunities/{opportunity["id"]}/notes',
                    bodyCfg={
                        'value': note},
                    isJSON=True,
                    method='POST'
                )
                note = resp.get('data')
                if not note:
                    errorMsg = resp.get('message')
                    return f'Error saving candidate opportunity to Lever: {errorMsg}'
            except ConnectionError:
                return LeverOpportunities.CONNECTION_ERROR_MSG

        return None


class LeverPostings(BaseLeverAPIView):

    @atomic
    def post(self, request, employerId=None):
        from upapp.apis.employer import JobPostingView  # Avoid circular import

        postings = getLeverItems('postings', self.employer)
        currentLeverJobs = {
            j.leverPostingKey: j for j in
            JobPostingView.getEmployerJobs(employerId=self.employer.id, jobFilter=Q(leverPostingKey__isnull=False))
        }
        roleLevels = {(r.role.name.lower(), r.roleLevelBit): r for r in RoleLevel.objects.prefetch_related('role').all()}

        processedLeverKeys = []
        for posting in postings:
            if LEVER_UPROVE_TAG not in posting['tags']:
                continue

            leverPostingKey = posting['id']
            processedLeverKeys.append(leverPostingKey)

            if not (currentJob := currentLeverJobs.get(leverPostingKey)):
                currentJob = EmployerJob(
                    employer=self.employer,
                    createdDateTime=timezone.now(),
                    modifiedDateTime=timezone.now(),
                    leverPostingKey=leverPostingKey
                )
                currentLeverJobs[leverPostingKey] = currentJob
            isUpdated = dataUtil.setObjectAttributes(currentJob, posting, {
                'jobTitle': {'formName': 'text'},
            }) or dataUtil.setObjectAttributes(currentJob, posting['categories'], {
                'jobDepartment': {'formName': 'team'},
                'isFullTime': {'formName': 'commitment', 'propFunc': lambda x: (not x) or ('full' in x.lower())},
                'location': None
            })
            currentJob.roleLevel = normalizeJobTitle(currentJob.jobTitle, roleLevels)

            jobLists = []
            for jobList in posting['content']['lists']:
                jobLists.append(f'<h5>{jobList["text"]}</h5>')
                jobLists.append(f'<ul>{jobList["content"]}</ul>')
            jobDescription = posting['content']['descriptionHtml'] + ''.join(jobLists) + posting['content'][
                'closingHtml']
            isUpdated = updateAndGetIsChanged(currentJob, 'jobDescription', jobDescription) or isUpdated

            state = posting['state']
            isConfidential = posting['confidentiality'] == 'confidential'
            isUpdated = updateAndGetIsChanged(currentJob, 'isInternal',
                                              state == 'internal' or isConfidential) or isUpdated

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


class LeverUsers(BaseLeverAPIView):

    def post(self, request, employerId=None):
        from upapp.apis.user import UserView  # Avoid circular import
        from upapp.viewsAuth import updateUproveUser
        uproveUsers = UserView.getUsers(filter=Q(employer_id=self.employer.id))
        for user in uproveUsers:
            leverUser = getLeverRequestWithRefresh(self.employer, f'/users?email={user.email}').get('data')
            if leverUser and not user.leverUserKey:
                user.leverUserKey = leverUser[0]['id']
                user.save()
            updateUproveUser(request)

        return Response(status=status.HTTP_200_OK)


class LeverStages(BaseLeverAPIView):

    def get(self, request, stageId=None, employerId=None):
        relativeUrl = f'stages/{stageId}' if stageId else 'stages'
        response = getLeverRequestWithRefresh(self.employer, relativeUrl)
        return Response(status=status.HTTP_200_OK, data=response.get('data', []))

    @staticmethod
    def getStage(employer, stageId):
        return getLeverRequestWithRefresh(employer, f'stages/{stageId}')

    @staticmethod
    def getAllStages(employer):
        return getLeverRequestWithRefresh(employer, 'stages')


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

    def validateRequest(self, request, hookAttr, employerId=None):
        data = request.data
        if not employerId:
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        self.employer = Employer.objects.get(id=employerId)
        hookKey = getattr(self.employer, hookAttr)
        if not hookKey:
            return Response('The signature token for this webhook has not been configured',
                            status=status.HTTP_400_BAD_REQUEST)

        isAuthorizedRequest = validateLeverRequest(data, hookKey)
        if not isAuthorizedRequest:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # If data is empty, it was just a test connection
        if not data['data']:
            return Response(status=status.HTTP_200_OK)

        return data['data']


class LeverChangeStage(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, 'leverHookStageChangeToken', employerId=employerId)
        if isinstance(data, Response):
            return data

        stage = LeverStages.getStage(self.employer, data['toStageId'])
        if not stage:
            return Response('No stage ID provided', status=status.HTTP_400_BAD_REQUEST)

        stageText = stage['data']['text'].lower()

        if stageText in ('new lead', 'reached out'):
            uproveStage = UserJobApplication.Status.INVITED.name
        elif stageText == 'new applicant':
            uproveStage = UserJobApplication.Status.APPROVED_NO_INTERVIEW.name
        elif stageText in ('phone screen', 'on-site interview', 'reference check'):
            uproveStage = UserJobApplication.Status.APPROVED_INTERVIEW.name
        elif stageText == 'offer':
            uproveStage = UserJobApplication.Status.OFFER.name
        else:
            uproveStage = UserJobApplication.Status.INVITED.name

        opportunityId = data["opportunityId"]

        try:
            jobApplication = UserJobApplication.objects.get(leverOpportunityKey=opportunityId)
            jobApplication.updateApplicationStatus(uproveStage, timezone.now())
            jobApplication.save()
        except UserJobApplication.DoesNotExist:
            pass

        return Response(status=status.HTTP_200_OK)


class LeverArchive(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, 'leverHookArchive', employerId=employerId)
        if isinstance(data, Response):
            return data

        # Do nothing if candidate is being unarchived
        if not bool(data['toArchived']):
            return Response(status=status.HTTP_200_OK)

        archivedReasonCode = data['toArchived']['reason']
        archiveReason = getLeverRequestWithRefresh(
            self.employer,
            f'archive_reasons/{archivedReasonCode}'
        )['data']['text']
        isHired = archiveReason.lower() == 'hired'

        try:
            jobApplication = UserJobApplication.objects.get(leverOpportunityKey=data['opportunityId'])
        except UserJobApplication.DoesNotExist:
            # This is not an application that we are tracking
            return Response(status=status.HTTP_200_OK)

        if isHired:
            jobApplication.updateApplicationStatus(UserJobApplication.Status.HIRED.name, timezone.now())
        else:
            jobApplication.updateApplicationStatus(UserJobApplication.Status.DECLINED.name, timezone.now())

        jobApplication.save()
        return Response(status=status.HTTP_200_OK)


class LeverHired(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, 'leverHookHired', employerId=employerId)
        if isinstance(data, Response):
            return data

        try:
            jobApplication = UserJobApplication.objects.get(leverOpportunityKey=data['opportunityId'])
        except UserJobApplication.DoesNotExist:
            # This is not an application that we are tracking
            return Response(status=status.HTTP_200_OK)

        jobApplication.updateApplicationStatus(UserJobApplication.Status.HIRED.name, timezone.now())
        jobApplication.save()

        return Response(status=status.HTTP_200_OK)


class LeverDeleted(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, 'leverHookDeleted', employerId=employerId)
        if isinstance(data, Response):
            return data

        try:
            jobApplication = UserJobApplication.objects.get(leverOpportunityKey=data['opportunityId'])
        except UserJobApplication.DoesNotExist:
            # This is not an application that we are tracking
            return Response(status=status.HTTP_200_OK)

        jobApplication.updateApplicationStatus(UserJobApplication.Status.DECLINED.name, timezone.now())
        jobApplication.save()

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


def getLeverRequestWithRefresh(employer, relativeUrl, nextKey=None, method='GET', bodyCfg=None, isJSON=False):
    body = {}  # {'responseType': 'json'}
    if bodyCfg:
        body = {**bodyCfg, **body}
    if nextKey:
        body['offset'] = nextKey
    url = f'{settings.LEVER_BASE_URL}{relativeUrl}'
    if method == 'GET':
        requestMethodFn = requests.get
    elif method == 'POST':
        requestMethodFn = requests.post
    else:
        requestMethodFn = requests.put

    headers = {'Authorization': f'Bearer {employer.leverAccessToken}'}
    if isJSON:
        headers = {**headers, 'Content-Type': 'application/json'}
    requestKwargs = {'headers': headers}
    if isJSON:
        requestKwargs['json'] = body
    else:
        requestKwargs['data'] = body

    response = requestMethodFn(url, **requestKwargs)

    # Update the access tokens if they have expired
    if (not is200Code(response)) and response.reason != 'Bad Request':
        response = requests.post(settings.LEVER_AUTH_TOKEN_URL, {
            'client_id': settings.LEVER_CLIENT_ID,
            'client_secret': settings.LEVER_CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': employer.leverRefreshToken
        })

        if not is200Code(response):
            raise ConnectionError()

        data = response.json()
        employer.leverAccessToken = data['access_token']
        employer.leverRefreshToken = data.get('refresh_token')
        employer.save()
        response = requestMethodFn(url, **requestKwargs)

    return response.json()


def is200Code(response):
    return 300 > response.status_code >= 200


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


def getLeverContact(employer, contactId):
    if not contactId:
        return {}
    contactData = getLeverRequestWithRefresh(employer, f'contacts/{contactId}')
    return serializeLeverContact(contactData)


def serializeLeverContact(contactData):
    return {
        'name': contactData['name'],
        'email': contactData['email'],
        'phoneNumbers': contactData.get('phones')
    }


def _getLeverConnectionErrorPage(request):
    from upapp.views import _getErrorPage  # Avoid circular import
    return _getErrorPage(
        request, status.HTTP_400_BAD_REQUEST,
        f'Uprove no longer has permission to access your Lever account. Please visit the integrations tab on your Uprove dashboard to reset the connection.'
    )
