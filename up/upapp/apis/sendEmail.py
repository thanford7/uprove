import base64
import urllib.request
from datetime import datetime
import logging
from http import HTTPStatus

import pytz
from django.conf import settings
from django.db.transaction import atomic
from django.template import loader
from django.templatetags.static import static
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from sendgrid import SendGridAPIClient, Attachment, ContentId, Disposition, FileType, FileName, FileContent
from sendgrid.helpers.mail import Mail

from upapp.apis import UproveAPIView
from upapp.models import EmployerInterest


TEST_EMAIL_ADDRESS = 'test@uprove.co'
sg = SendGridAPIClient(settings.SENDGRID_API_KEY)

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python


def sendSgEmail(message: Mail):
    try:
        response = sg.send(message)
        return response
    except Exception as e:
        logging.log(logging.ERROR, e.message)
        return False


class EmailView(UproveAPIView):
    permission_classes = [AllowAny]

    TYPE_CONTACT = 'CONTACT'
    TYPE_EMPLOYER_INTEREST = 'EMPLOYER_INTEREST'
    TYPE_CANDIDATE_SIGNUP = 'CANDIDATE_SIGNUP'
    TYPE_CANDIDATE_INTEREST = 'CANDIDATE_INTEREST'

    SEND_EMAIL_ADDRESS = 'no_reply@uprove.co'  # Email address where all emails originate from

    EMAIL_ROUTES = {
        TYPE_CONTACT: 'info@uprove.co',
        TYPE_EMPLOYER_INTEREST: 'sales@uprove.co',
        TYPE_CANDIDATE_SIGNUP: 'community@uprove.co',
        TYPE_CANDIDATE_INTEREST: 'info@uprove.co'
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
    def sendEmail(subjectText, toEmails, djangoContext=None, djangoEmailBodyTemplate=None, htmlContent=None, fromEmail=None, ccEmail=None):
        """Blend SendGrid's email service with Django's email templates
        :param subjectText {str}: The email subject line
        :param toEmails {list}:
        :param djangoContext {dict}: Key/value pairs that can be accessed in the djangoEmailBody
        :param djangoEmailBodyTemplate {str}: Email template path to be used for the body. Can be null if htmlContent is
        provided directly
        :param htmlContent {str}: Html string that has already been formatted
        :param fromEmail {str}: If not provided, the default no reply email will be used
        :return: SendGrid email response
        """
        subject = ''.join(subjectText.splitlines())  # Email subject *must not* contain newlines
        htmlContent = htmlContent or loader.render_to_string(djangoEmailBodyTemplate, djangoContext)

        message = Mail(
            from_email=fromEmail or EmailView.SEND_EMAIL_ADDRESS,
            to_emails=toEmails if not settings.DEBUG else TEST_EMAIL_ADDRESS,
            subject=subject,
            html_content=htmlContent)

        if ccEmail and not settings.DEBUG:
            if not isinstance(ccEmail, list):
                ccEmail = [ccEmail]
            for email in ccEmail:
                message.add_cc(email)

        # Add Uprove logo
        imageName = 'logo.png'
        imageUrl = static(f'img/{imageName}')
        fileOpenner = lambda url: urllib.request.urlopen(url)
        if settings.DEBUG:
            imageUrl = f'up{imageUrl}'
            fileOpenner = lambda url: open(url, 'rb')
        with fileOpenner(imageUrl) as logoFile:
            encodedLogo = base64.b64encode(logoFile.read()).decode()
            message.attachment = Attachment(FileContent(encodedLogo),
                                            FileName(imageName),
                                            FileType('image/png'),
                                            Disposition('inline'),
                                            ContentId('logo'))

        return sendSgEmail(message)

    @staticmethod
    def sendFormattedEmail(request, contactType=None):
        contactType = contactType or request.data['type']
        userSubject = None
        userContent = None
        userEmail = None
        if contactType == EmailView.TYPE_CONTACT:
            subject = 'New question or request for help'
            content = _generateEmailBody(request.data, (
                ('Name', 'name'),
                ('Email', 'fromEmail'),
                ('Company', 'company'),
                ('Message', 'message')
            ))

            userSubject = 'Uprove | Thanks for your question'
            userContent = 'Thank you for your question. Our support team will respond within 24 hours.'
            userEmail = request.data['fromEmail']
        elif contactType == EmailView.TYPE_EMPLOYER_INTEREST:
            _saveEmployerInterest(request.data)
            subject = 'New employer interest!'
            content = _generateEmailBody(request.data, (
                ('First name', 'firstName'),
                ('Last name', 'lastName'),
                ('Email', 'fromEmail'),
                ('Company', 'companyName'),
                ('Note', 'note')
            ))

            userSubject = 'Uprove | Thanks for your interest'
            userContent = 'We are excited to explore how we can partner with you and show you the hidden talent you\'re missing.' \
                          ' Our team will respond within 24 hours to find time to understand your challenges and demo the product.'
            userEmail = request.data['fromEmail']
        elif contactType == EmailView.TYPE_CANDIDATE_SIGNUP:
            subject = 'New user signup!'
            content = _generateEmailBody(request.data, (
                ('First name', 'firstName'),
                ('Last name', 'lastName'),
                ('Email', 'email')
            ))
            userEmail = request.data['email']
        elif contactType == EmailView.TYPE_CANDIDATE_INTEREST:
            subject = 'New candidate interest!'
            content = _generateEmailBody(request.data, (
                ('Email', 'email'),
                ('Interest type', 'interestType')
            ))
            userSubject = 'Uprove | Thanks for your interest'
            userContent = 'Thank you for your interest. One of our talent advocates will contact you within 24 hours to' \
                          ' answer your questions and show you how we can help you land your next job!'
            userEmail = request.data['email']
        else:
            logging.log(logging.ERROR, f'Unknown contact type of {contactType}')
            return Response(status=HTTPStatus.BAD_REQUEST)

        if not userEmail:
            return Response('An email address is required', status=HTTPStatus.BAD_REQUEST)

        response = EmailView.sendEmail(
            subject, EmailView.EMAIL_ROUTES[contactType], htmlContent=content
        )

        if userSubject:
            EmailView.sendEmail(
                userSubject,
                [userEmail],
                djangoContext={'bodyContent': userContent},
                djangoEmailBodyTemplate='email/generalEmail.html'
            )

        return response


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
        employerInterest.companyName = data['companyName']
        employerInterest.note = data.get('note')
        employerInterest.modifiedDateTime = datetime.now(tz=pytz.UTC)
        employerInterest.save()
    except EmployerInterest.DoesNotExist:
        employerInterest = EmployerInterest(
            firstName=data.get('firstName'),
            lastName=data.get('lastName'),
            email=data['fromEmail'],
            companyName=data.get('companyName'),
            note=data.get('note'),
            createdDateTime=datetime.now(tz=pytz.UTC),
            modifiedDateTime=datetime.now(tz=pytz.UTC)
        )
        employerInterest.save()
