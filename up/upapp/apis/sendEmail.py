import logging
from http import HTTPStatus

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.conf import settings


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
    generateRow = lambda name, key: f'<tr><td><strong>{name}</strong></td><td>{data[key]}</td></tr>'
    return '<table>' + ''.join((generateRow(*row) for row in emailRows)) + '</table>'
