from datetime import datetime
import logging
from http import HTTPStatus

import pytz
from django.conf import settings
from django.db import models
from django.db.transaction import atomic
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from upapp.models import CandidateInterest, EmployerInterest, ProjectFunction, ProjectSkill


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
    TYPE_CANDIDATE_SIGNUP = 'CANDIDATE_SIGNUP'

    SEND_EMAIL_ADDRESS = 'no_reply@uprove.co'  # Email address where all emails originate from

    EMAIL_ROUTES = {
        TYPE_CONTACT: 'info@uprove.co',
        TYPE_EMPLOYER_INTEREST: 'sales@uprove.co',
        TYPE_CANDIDATE_SIGNUP: 'community@uprove.co'
    }

    def post(self, request, contactType=None):
        response = self.sendFormattedEmail(request, contactType=contactType)
        if isinstance(response, Response):
            return response
        elif response:
            logging.log(logging.INFO, response)
            return Response(status=HTTPStatus.OK)
        else:
            raise Exception('An error occurred while sending the email')

    @staticmethod
    def sendFormattedEmail(request, contactType=None):
        contactType = contactType or request.data['type']
        if contactType == EmailView.TYPE_CONTACT:
            subject = 'New question or request for help'
            content = _generateEmailBody(request.data, (
                ('Name', 'name'),
                ('Email', 'fromEmail'),
                ('Company', 'company'),
                ('Message', 'message')
            ))
        elif contactType == EmailView.TYPE_EMPLOYER_INTEREST:
            _saveEmployerInterest(request.data)
            subject = 'New employer interest!'
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
        elif contactType == EmailView.TYPE_CANDIDATE_SIGNUP:
            subject = 'New user signup!'
            content = _generateEmailBody(request.data, (
                ('First name', 'firstName'),
                ('Last name', 'lastName'),
                ('Email', 'email')
            ))
        else:
            logging.log(logging.ERROR, f'Unknown contact type of {contactType}')
            return Response(status=HTTPStatus.BAD_REQUEST)
        message = Mail(
            from_email=EmailView.SEND_EMAIL_ADDRESS,
            to_emails=EmailView.EMAIL_ROUTES[contactType] if not settings.DEBUG else TEST_EMAIL_ADDRESS,
            subject=subject,
            html_content=content)

        return sendEmail(message)

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
            firstName=data.get('firstName'),
            lastName=data.get('lastName'),
            email=data['fromEmail'],
            title=data.get('title'),
            companyName=data.get('companyName'),
            companyEmployeeCount=data.get('size'),
            note=data.get('note'),
            createdDateTime=datetime.now(tz=pytz.UTC),
            modifiedDateTime=datetime.now(tz=pytz.UTC)
        )
        employerInterest.save()

    _saveProjectTags(data, employerInterest, 'hiringFunctions', 'hiringSkills')


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
