import names
from django.contrib.auth.models import User as DjangoUser
from django.test import TestCase
from django.utils import crypto, timezone
from rest_framework.test import APIClient

from upapp.apis import ActivityKey
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
        self.client = APIClient()
        self.users = [createUser() for _ in range(4)]
        self.companySizes = createCompanySizes()
        self.states = createStates()
        self.countries = createCountries()
        self.roles = createRoles()
        self.roleLevels = createRoleLevels()
        self.employers = [createEmployer(name) for name in ['Google', 'Microsoft', 'Pizza Hit']]
        self.employerJobs = [createEmployerJob(title) for title in ['Product manager', 'Senior customer success mgr']]
        createActivities()

        self.loginAdmin()

    def loginAdmin(self):
        password = 'uproveAdmin1'
        email = 'admin_1@uprove.co'
        self.adminUser = createUser(
            email=email,
            password=password,
            userTypeBits=User.USER_TYPE_CANDIDATE | User.USER_TYPE_EMPLOYER | User.USER_TYPE_ADMIN
        )
        resp = self.makeRequest('login/', self.REQUEST_POST, data={'email': email, 'password': password})
        return resp

    def makeRequest(self, url, requestType, data=None, isApi=True):
        if isApi:
            url = f'/{self.apiPath}{url}'

        if requestType == self.REQUEST_GET:
            return self.client.get(url, data)
        elif requestType == self.REQUEST_POST:
            return self.client.post(url, data=data)
        elif requestType == self.REQUEST_PUT:
            return self.client.put(url, data=data)


def createActivities():
    for activity in ActivityKey:
        activityKey = activity.name
        Activity(key=activityKey, name=activityKey).save()


def createCompanySizes():
    sizes = []
    for size in ['<50', '50-100', '101-250', '251-500', '501-1000', '1001+']:
        coSize = CompanySize(companySize=size)
        coSize.save()
        sizes.append(coSize)

    return sizes


def createStates():
    states = []
    for stateName in ['Colorado', 'Wyoming', 'Nebraska', 'North Dakota']:
        state = State(stateName=stateName)
        state.save()
        states.append(state)

    return states


def createCountries():
    countries = []
    for countryName in ['USA', 'UK']:
        country = Country(countryName=countryName)
        country.save()
        countries.append(country)

    return countries


def createRoles():
    roles = []
    for roleName in ['Product Management', 'Project Management', 'Customer Success']:
        role = Role(name=roleName)
        role.save()
        roles.append(role)

    return roles


def createRoleLevels():
    roleLevels = []
    for role in Role.objects.all():
        for level in [1, 2]:
            roleLevel = RoleLevel(
                role=role,
                roleLevelBit=level,
                roleTitle=f'{role.name} - {level}'
            )
            roleLevel.save()
            roleLevels.append(roleLevel)

    return roleLevels


def createEmployer(companyName, **kwargs):
    employer = Employer(
        companyName=companyName,
        companySize=kwargs.get('companySize') or CompanySize.objects.all()[0],
        isDemo=kwargs.get('isDemo') or False,
        isClient=kwargs.get('isClient') or True,
        createdDateTime=timezone.now(),
        modifiedDateTime=timezone.now()
    )

    employer.save()
    return employer


def createEmployerJob(jobTitle, **kwargs):
    job = EmployerJob(
        employer=kwargs.get('employer') or Employer.objects.all()[0],
        jobTitle=jobTitle,
        jobDescription=kwargs.get('description') or 'This is the best job in the world',
        openDate=kwargs.get('openDate') or timezone.now(),
        closeDate=kwargs.get('closeDate') or None,
        isRemote=kwargs.get('isRemote') or False,
        city=kwargs.get('city') or 'Denver',
        state=kwargs.get('state') or State.objects.all()[0],
        country=kwargs.get('country') or Country.objects.all()[0],
        roleLevel=kwargs.get('roleLevel') or RoleLevel.objects.all()[0],
        createdDateTime=timezone.now(),
        modifiedDateTime=timezone.now()
    )

    job.save()
    return job


def createUser(**kwargs):
    firstName = kwargs.get('firstName') or names.get_first_name()
    lastName = kwargs.get('lastName') or names.get_last_name()
    email = kwargs.get('email') or f'{firstName}_{lastName}@uprove.co'

    djangoUserKwargs = dict(
        email=email,
        first_name=firstName,
        last_name=lastName,
        password=kwargs.get('password') or generatePassword()
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
