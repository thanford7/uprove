import names
from django.contrib.auth.models import User as DjangoUser
from django.test import Client, TestCase
from django.utils import crypto, timezone

from upapp.models import *
from upapp.urls import apiPath


def generatePassword():
    return crypto.get_random_string(length=30, allowed_chars=crypto.RANDOM_STRING_CHARS + '!@#$%^&*()-+=')


class BaseTest(TestCase):
    apiPath = apiPath
    REQUEST_GET = 'GET'
    REQUEST_POST = 'POST'
    REQUEST_PUT = 'PUT'

    def setUp(self) -> None:
        self.client = Client()
        self.users = [createUser() for _ in range(4)]

    def makeRequest(self, url, requestType, data=None, isApi=True):
        if isApi:
            url = f'/{self.apiPath}{url}'

        requestMethod = self.client.get
        if requestType == self.REQUEST_POST:
            requestMethod = self.client.post
        elif requestType == self.REQUEST_PUT:
            requestMethod = self.client.put

        return requestMethod(url, data)


def createUser(**kwargs):
    firstName = kwargs.get('firstName') or names.get_first_name()
    lastName = kwargs.get('lastName') or names.get_last_name()
    email = f'{firstName}_{lastName}@uprove.co'

    djangoUserKwargs = dict(
        email=email,
        first_name=firstName,
        last_name=lastName,
        password=generatePassword()
    )
    djangoUser = DjangoUser.objects.create_user(email, **djangoUserKwargs)

    user = User(
        djangoUser=djangoUser,
        firstName=firstName,
        lastName=lastName,
        email=email,
        employer_id=kwargs.get('employerId'),
        createdDateTime=timezone.now(),
        modifiedDateTime=timezone.now()
    )

    if userTypeBits := kwargs.get('userTypeBits'):
        user.userTypeBits = userTypeBits

    user.save()

    return user
