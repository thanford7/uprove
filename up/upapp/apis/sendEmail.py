from datetime import datetime
import logging
from http import HTTPStatus

import pytz
from django.db import models
from django.db.transaction import atomic
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.conf import settings
from ..models import CandidateInterest, EmployerInterest, ProjectFunction, ProjectSkill


TEST_EMAIL_ADDRESS = 'test@uprove.co'
sg = SendGridAPIClient(settings.SENDGRID_API_KEY)

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python


def sendEmail(message: Mail):
    try:
        response = sg.send(message)
        return response
    except Exception as e:
        logging.log(logging.ERROR, e.message)
        return False


class EmailView(APIView):
    permission_classes = [AllowAny]

    TYPE_CONTACT = 'CONTACT'
    TYPE_EMPLOYER_INTEREST = 'EMPLOYER_INTEREST'
    TYPE_CANDIDATE_INTEREST = 'CANDIDATE_INTEREST'

    SEND_EMAIL_ADDRESS = 'no_reply@uprove.co'  # Email address where all emails originate from

    EMAIL_ROUTES = {
        TYPE_CONTACT: 'info@uprove.co',
        TYPE_EMPLOYER_INTEREST: 'sales@uprove.co',
        TYPE_CANDIDATE_INTEREST: 'community@uprove.co'
    }

    def post(self, request):
        contactType = request.data['type']
        if contactType == self.TYPE_CONTACT:
            content = _generateEmailBody(request.data, (
                ('Name', 'name'),
                ('Email', 'fromEmail'),
                ('Company', 'company'),
                ('Message', 'message')
            ))
        elif contactType == self.TYPE_EMPLOYER_INTEREST:
            _saveEmployerInterest(request.data)
            content = _generateEmailBody(request.data, (
                ('First name', 'firstName'),
                ('Last name', 'lastName'),
                ('Email', 'fromEmail'),
                ('Job title', 'title'),
                ('Company', 'companyName'),
                ('Company employee count', 'size'),
                ('Hiring for roles', 'roleFunctions'),
                ('Hiring for skills', 'roleSkills'),
                ('Note', 'note')
            ))
        elif contactType == self.TYPE_CANDIDATE_INTEREST:
            _saveCandidateInterest(request.data)
            content = _generateEmailBody(request.data, (
                ('First name', 'firstName'),
                ('Last name', 'lastName'),
                ('Email', 'fromEmail'),
                ('LinkedIn link', 'linkedInLink'),
                ('Interested in roles', 'roleFunctions'),
                ('Current skills', 'roleSkills'),
                ('Referrer', 'referrer'),
                ('Note', 'note')
            ))
        else:
            logging.log(logging.ERROR, f'Unknown contact type of {contactType}')
            return Response(status=HTTPStatus.BAD_REQUEST)
        message = Mail(
            from_email=self.SEND_EMAIL_ADDRESS,
            to_emails=self.EMAIL_ROUTES[contactType] if not settings.DEBUG else TEST_EMAIL_ADDRESS,
            subject=request.data.get('subject', 'Unknown subject'),
            html_content=content)
        if response := sendEmail(message):
            logging.log(logging.INFO, response)
            return Response(status=HTTPStatus.OK)
        else:
            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


def _generateEmailBody(data: dict, emailRows: tuple):
    return '<table>' + ''.join((_generateEmailTableRow(data, *row) for row in emailRows)) + '</table>'


def _generateEmailTableRow(data, name, key):
    val = data.get(key, None)
    if isinstance(val, list):
        val = '<ul style="margin:0; margin-left: 25px; padding:0;">' + ''.join((f'<li>{li}</li>' for li in val)) + '</ul>'
    return f'''
        <tr>
            <td style="border: solid 1px #e9e9e9;"><strong>{name}</strong></td>
            <td style="border: solid 1px #e9e9e9;">{val}</td>
        </tr>
    '''


@atomic
def _saveEmployerInterest(data: dict):
    try:
        employerInterest = EmployerInterest.objects.get(email=data['fromEmail'])
        employerInterest.firstName = data['firstName']
        employerInterest.lastName = data['lastName']
        employerInterest.title = data['title']
        employerInterest.companyName = data['companyName']
        employerInterest.companyEmployeeCount = data.get('size')
        employerInterest.note = data.get('note')
        employerInterest.modifiedDateTime = datetime.now(tz=pytz.UTC)
        employerInterest.hiringFunctions.clear()
        employerInterest.hiringSkills.clear()
        employerInterest.save()
    except EmployerInterest.DoesNotExist:
        employerInterest = EmployerInterest(
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['fromEmail'],
            title=data['title'],
            companyName=data['companyName'],
            companyEmployeeCount=data.get('size'),
            note=data.get('note'),
            createdDateTime=datetime.now(tz=pytz.UTC),
            modifiedDateTime=datetime.now(tz=pytz.UTC)
        )
        employerInterest.save()

    _saveProjectTags(data, employerInterest, 'hiringFunctions', 'hiringSkills')


@atomic
def _saveCandidateInterest(data: dict):
    try:
        candidateInterest = CandidateInterest.objects.get(email=data['fromEmail'])
        candidateInterest.firstName = data['firstName']
        candidateInterest.lastName = data['lastName']
        candidateInterest.linkedInProfile = data['linkedInLink']
        candidateInterest.referrer = data.get('referrer')
        candidateInterest.note = data.get('note')
        candidateInterest.modifiedDateTime = datetime.now(tz=pytz.UTC)
        candidateInterest.interestedFunctions.clear()
        candidateInterest.currentSkills.clear()
        candidateInterest.save()
    except CandidateInterest.DoesNotExist:
        candidateInterest = CandidateInterest(
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['fromEmail'],
            linkedInProfile=data['linkedInLink'],
            referrer=data.get('referrer'),
            note=data.get('note'),
            createdDateTime=datetime.now(tz=pytz.UTC),
            modifiedDateTime=datetime.now(tz=pytz.UTC)
        )
        candidateInterest.save()

    _saveProjectTags(data, candidateInterest, 'interestedFunctions', 'currentSkills')


def _saveProjectTags(data: dict, modelInstance: models.Model, roleFunctionAttr: str, roleSkillAttr: str):
    existingRfs = {pf.functionName: pf for pf in ProjectFunction.objects.all()}
    for roleFunction in data.get('roleFunctions', []):
        if not (rf := existingRfs.get(roleFunction)):
            rf = ProjectFunction(functionName=roleFunction)
            rf.save()
        getattr(modelInstance, roleFunctionAttr).add(rf)

    existingRss = {ps.skillName: ps for ps in ProjectSkill.objects.all()}
    for roleSkill in data.get('roleSkills', []):
        if not (rs := existingRss.get(roleSkill)):
            rs = ProjectSkill(skillName=roleSkill)
            rs.save()
        getattr(modelInstance, roleSkillAttr).add(rs)
