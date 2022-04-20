import hashlib
import hmac
import os
from json import dumps
from urllib import parse

import requests
from datetime import datetime, timedelta

import bs4
from django.db.models import Q
from django.db.transaction import atomic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp import security
from upapp.apis import UproveAPIView
from upapp.apis.employer import JobPostingView
from upapp.apis.project import ProjectView
from upapp.apis.sendEmail import EmailView
from upapp.models import Employer, EmployerJob, RoleTitle, User, UserJobApplication
from upapp.modelSerializers import getSerializedProject, getSerializedCustomProject
from upapp.scraper.scraper.utils.normalize import normalizeJobTitle
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


def leverCustomizeAssessment(request, employerId=None, opportunityId=None):
    from upapp.views import _getErrorPage  # Avoid circular import
    # TODO: Require login to access page
    if not opportunityId:
        return _getErrorPage(request, status.HTTP_400_BAD_REQUEST, 'An opportunity ID is required')

    if not employerId:
        return _getErrorPage(request, status.HTTP_400_BAD_REQUEST, 'An employer ID is required')

    employer = Employer.objects.get(id=employerId)
    try:
        opportunity = getLeverRequestWithRefresh(
            employer,
            f'opportunities/{opportunityId}?expand=applications&expand=owner&expand=followers&expand=sourcedBy'
        )['data']
    except ConnectionError:
        return _getLeverConnectionErrorPage(request)

    postingKey = opportunity['applications'][0]['posting']

    try:
        posting = getLeverRequestWithRefresh(
            employer,
            f'postings/{postingKey}'
        )['data']
    except ConnectionError:
        return _getLeverConnectionErrorPage(request)

    try:
        uproveJob = EmployerJob.objects\
            .prefetch_related('allowedProjects', 'allowedProjects__project', 'allowedProjects__skills')\
            .get(leverPostingKey=postingKey)
        allowedProjects = sorted(uproveJob.allowedProjects.all(), key=lambda p: p.id)
        primaryProject = allowedProjects[0] if allowedProjects else None
    except EmployerJob.DoesNotExist:
        return _getErrorPage(
            request, status.HTTP_400_BAD_REQUEST,
            f'Job posting not found.'
        )

    contacts = {}
    for idx, contactData in enumerate([opportunity['owner']] + opportunity['followers'] + [opportunity['sourcedBy']]):
        if not contacts.get(contactData['id']):
            contacts[contactData['id']] = {**serializeLeverContact(contactData), 'priority': idx}

    return render(request, 'leverSendOpportunity.html', context={
        'data': dumps({
            'candidate': {
                'name': opportunity['name'],
                'emails': opportunity['emails'],
                'contacts': sorted(contacts.values(), key=lambda x: x['priority']),
                'tags': opportunity['tags'],
                'opportunityId': opportunityId
            },
            'employer': {
                'id': employer.id,
                'companyName': employer.companyName,
                'logo': employer.logo.url if employer.logo else None,
            },
            'jobId': uproveJob.id,
            'jobTitle': posting['text'],
            'primaryCustomProject': getSerializedCustomProject(primaryProject) if primaryProject else None,
            'projects': [getSerializedProject(p) for p in ProjectView.getProjects(employerId=employer.id)]
        })
    })


class LeverSendAssessment(UproveAPIView):

    @atomic
    def post(self, request):
        from upapp.apis.user import UserView, UprovePasswordResetForm  # Avoid circular import
        user = None
        htmlBody = self.data['emailBody']
        for userEmail in self.data['candidateEmails']:
            try:
                user = User.objects.get(email=userEmail)
                if user:
                    break
            except User.DoesNotExist:
                continue

        if not user:
            candidateNames = self.data['candidateName'].split(' ')
            firstName = candidateNames[0]
            lastName = ' '.join(candidateNames[1:]) if len(candidateNames) > 1 else ''
            user, _ = UserView.createUser({
                'email': self.data['candidateEmails'][0],
                'firstName': firstName,
                'lastName': lastName,
                'inviteEmployerId': self.data['employerId']
            }, False)
            resetContext = UprovePasswordResetForm({'email': user.email}).getEmailContext(request, user.email)
            htmlBody = bs4.BeautifulSoup(htmlBody)
            redirectLink = htmlBody.find(id='redirectLink')
            originalRedirectLink = redirectLink['href']
            urlParams = {'isnew': False, 'next': originalRedirectLink}
            encodedUrlParams = parse.urlencode(urlParams)
            redirectLink[
                'href'] = f'{resetContext["protocol"]}://{resetContext["domain"]}/password-reset-email/{resetContext["uid"]}/{resetContext["token"]}/?{encodedUrlParams}'
            htmlBody = str(htmlBody)

        job = JobPostingView.getEmployerJobs(jobId=self.data['jobId'])
        JobPostingView.setCustomProjects(job, [self.data['customProject']], isDeleteExisting=False)

        # Create an application for the user if it doesn't exist
        leverOpportunityKey = self.data['opportunityId']
        try:
            UserJobApplication.objects.get(leverOpportunityKey=leverOpportunityKey)
        except UserJobApplication.DoesNotExist:
            UserJobApplication(
                user=user,
                employerJob=job,
                inviteDateTime=timezone.now(),
                leverOpportunityKey=leverOpportunityKey
            ).save()

        response = EmailView.sendEmail(
            self.data['emailTitle'],
            self.data['candidateEmails'],
            htmlContent=htmlBody,
            fromEmail=self.data['companyContactEmail'],
            ccEmail=[EmailView.EMAIL_ROUTES[EmailView.TYPE_CANDIDATE_SIGNUP], self.data['companyContactEmail']]
        )

        return Response(status=response.status_code)


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

        self.employer = Employer.objects.get(id=employerId)
        hookKey = getattr(self.employer, hookAttr)
        if not hookKey:
            return Response('The signature token for this webhook has not been configured', status=status.HTTP_400_BAD_REQUEST)

        isAuthorizedRequest = validateLeverRequest(data, hookKey)
        if not isAuthorizedRequest:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return data['data']


class LeverChangeStage(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, 'leverHookStageChangeToken', employerId=employerId)
        if isinstance(data, Response):
            return data

        if data['toStageId'] != self.employer.leverTriggerStageKey:
            return Response(status=status.HTTP_200_OK)

        opportunityId = data["opportunityId"]
        opportunity = getLeverRequestWithRefresh(self.employer, f'opportunities/{opportunityId}')['data']
        if LEVER_UPROVE_TAG not in opportunity['tags']:
            return Response(status=status.HTTP_200_OK)

        resp = getLeverRequestWithRefresh(
            self.employer,
            f'opportunities/{data["opportunityId"]}/addLinks',
            bodyCfg={'links': [request.build_absolute_uri(f'/lever/customize-assessment/{employerId}/{opportunityId}/'),]},
            isJSON=True,
            method='POST'
        )

        return Response(status=resp['status_code'])


class LeverArchive(BaseLeverChange):

    def post(self, request, employerId=None):
        data = self.validateRequest(request, 'leverHookArchive', employerId=employerId)
        if isinstance(data, Response):
            return data

        isHired = False
        wasHired = False
        if isArchived := bool(data['toArchived']):
            archivedReasonCode = data['toArchived']['reason']
            archiveReason = getLeverRequestWithRefresh(
                self.employer,
                f'archive_reasons/{archivedReasonCode}'
            )['data']['text']
            isHired = archiveReason.lower() == 'hired'
        if bool(data['fromArchived']):
            archivedReasonCode = data['fromArchived']['reason']
            archiveReason = getLeverRequestWithRefresh(
                self.employer,
                f'archive_reasons/{archivedReasonCode}'
            )['data']['text']
            wasHired = archiveReason.lower() == 'hired'

        try:
            jobApplication = UserJobApplication.objects.get(leverOpportunityKey=data['opportunityId'])
        except UserJobApplication.DoesNotExist:
            # This is not an application that we are tracking
            return Response(status=status.HTTP_200_OK)

        if isHired:
            isArchived = False
            jobApplication.approveDateTime = timezone.now()
            jobApplication.hireDateTime = timezone.now()
            jobApplication.declineDateTime = None
        elif wasHired:
            jobApplication.approveDateTime = None
            jobApplication.hireDateTime = None

        if isArchived and not jobApplication.declineDateTime:
            jobApplication.declineDateTime = timezone.now()

        if not isArchived and jobApplication.declineDateTime:
            jobApplication.declineDateTime = None

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

        jobApplication.approveDateTime = timezone.now()
        jobApplication.hireDateTime = timezone.now()
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

        if not jobApplication.declineDateTime:
            jobApplication.declineDateTime = timezone.now()
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
    url = f'{os.getenv("LEVER_BASE_URL")}{relativeUrl}'
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
    if response.status_code != 200 and response.reason != 'Bad Request':
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
        response = requestMethodFn(url, **requestKwargs)

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


def updateLeverAssessmentComplete(request, jobApplication):
    if opportunityKey := jobApplication.leverOpportunityKey:
        employer = jobApplication.employerJob.employer
        getLeverRequestWithRefresh(
            employer,
            f'opportunities/{opportunityKey}/addLinks',
            bodyCfg={'links': [
                request.build_absolute_uri('/employerDashboard/?tab=applications'), ]},
            isJSON=True,
            method='POST'
        )

        getLeverRequestWithRefresh(
            employer,
            f'opportunities/{opportunityKey}/notes',
            bodyCfg={
                'value': 'Candidate has completed the Uprove assessment. A link was added to this opportunity to view the assessment.'},
            isJSON=True,
            method='POST'
        )

        if newLeverStage := employer.leverCompleteStageKey:
            getLeverRequestWithRefresh(
                employer,
                f'opportunities/{opportunityKey}/stage',
                bodyCfg={'stage': newLeverStage},
                isJSON=True,
                method='PUT'
            )


def _getLeverConnectionErrorPage(request):
    from upapp.views import _getErrorPage  # Avoid circular import
    return _getErrorPage(
        request, status.HTTP_400_BAD_REQUEST,
        f'Uprove no longer has permission to access your Lever account. Please visit the integrations tab on your Uprove dashboard to reset the connection.'
    )
