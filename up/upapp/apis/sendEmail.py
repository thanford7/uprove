from datetime import datetime
import logging
from http import HTTPStatus

import pytz
from django.db import IntegrityError
from django.db.transaction import atomic
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.conf import settings
from ..models import EmployerInterest, ProjectFunction, ProjectSkill


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
            content = _generateEmailBody(request.data, (
                ('Todo', 'todo'),
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
    generateRow = lambda name, key: f'<tr><td><strong>{name}</strong></td><td>{data.get(key, None)}</td></tr>'
    return '<table>' + ''.join((generateRow(*row) for row in emailRows)) + '</table>'


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

    existingRfs = {pf.functionName: pf for pf in ProjectFunction.objects.all()}
    for roleFunction in data.get('roleFunctions', []):
        if not (rf := existingRfs.get(roleFunction)):
            rf = ProjectFunction(functionName=roleFunction)
            rf.save()
        employerInterest.hiringFunctions.add(rf)

    existingRss = {ps.skillName: ps for ps in ProjectSkill.objects.all()}
    for roleSkill in data.get('roleSkills', []):
        if not (rs := existingRss.get(roleSkill)):
            rs = ProjectSkill(skillName=roleSkill)
            rs.save()
        employerInterest.hiringSkills.add(rs)
