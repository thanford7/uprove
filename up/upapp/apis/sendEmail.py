import logging

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.conf import settings


sg = SendGridAPIClient(settings.SENDGRID_API_KEY)

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
# message = Mail(
#     from_email='from_email@uprove.co',
#     to_emails='to@example.com',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')


def sendEmail(message: Mail):
    try:
        response = sg.send(message)
        return response
    except Exception as e:
        logging.log(e.message)
        return e.message