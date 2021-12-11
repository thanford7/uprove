from http import HTTPStatus
from json import dumps

from django.shortcuts import render

from upapp import security
from upapp.modelSerializers import getSerializedProject, getSerializedEmployer, getSerializedUser, \
    getSerializedProjectSkill, getSerializedProjectFunction
from upapp.apis.employer import EmployerView
from upapp.apis.project import ProjectView
from upapp.apis.user import UserView, UserProfileView
from upapp.models import ProjectFunction, ProjectSkill


# Create your views here.
def homepage(request):
    return render(request, 'home.html', {'data': dumps({
        'functions': [getSerializedProjectFunction(f) for f in ProjectFunction.objects.all()],
        'skills': [getSerializedProjectSkill(s) for s in ProjectSkill.objects.all()]
    })})


def about(request):
    return render(request, 'about.html', context={})


def accountSettings(request, userId):
    if not security.isSelf(request, userId):
        return _getUnauthorizedPage(request)
    user = UserView.getUser(userId)
    serializedUser = {}
    if user:
        serializedUser = getSerializedUser(user)
    return render(request, 'accountSettings.html', {'data': dumps(serializedUser)})


def admin(request):
    if not security.isPermittedAdmin(request):
        return _getUnauthorizedPage(request)
    return render(request, 'admin.html', {'data': dumps({
        'projects': [getSerializedProject(p, isIncludeDetails=True) for p in ProjectView.getProjects(isIgnoreEmployerId=True)],
        # TODO: Lazy load employers and users since this will get long
        'employers': [getSerializedEmployer(e) for e in EmployerView.getEmployers()],
        'users': [getSerializedUser(u) for u in UserView.getUsers()],
        'functions': [getSerializedProjectFunction(f) for f in ProjectFunction.objects.all()],
        'skills': [getSerializedProjectSkill(s) for s in ProjectSkill.objects.all()]
    })})


def contact(request):
    return render(request, 'contact.html', context={})


def employerDashboard(request, employerId=None):
    user = security.getSessionUser(request)
    if not user:
        return _getUnauthorizedPage(request)

    employerId = employerId or user['employerId']
    if not employerId:
        return _getErrorPage(request, HTTPStatus.BAD_REQUEST, 'An employer ID is required')

    if not security.isPermittedEmployer(request, employerId):
        return _getUnauthorizedPage(request)

    return render(request, 'employerDashboard.html', context={'data': dumps({
        'employer': getSerializedEmployer(EmployerView.getEmployer(employerId)),
        'projects': [getSerializedProject(p, isIncludeDetails=True) for p in ProjectView.getProjects(employerId=employerId)],
    })})


def errors(request):
    return render(request, 'errors.html', context={})


def privacy(request):
    return render(request, 'privacy.html', context={})


def profile(request, profileId):
    profile = UserProfileView.getUserProfile(profileId)
    return render(request, 'userProfile.html', context={'data': UserProfileView.serializeUserProfile(profile)})


def profiles(request, userId):
    userProfiles = UserView.getUserProfiles(userId)
    if len(profiles := userProfiles.profile.all()) == 1:
        return render(request, 'userProfile.html', context={'data': UserProfileView.serializeUserProfile(profiles[0])})
    return render(request, 'userProfiles.html', context={'data': None})  # TODO


def project(request, projectId):
    return render(request, 'project.html', context={'data': dumps({
        'project': getSerializedProject(ProjectView.getProject(projectId), isIncludeDetails=security.isPermittedSessionUser(request)),
        'functions': [getSerializedProjectFunction(f) for f in ProjectFunction.objects.all()],
        'skills': [getSerializedProjectSkill(s) for s in ProjectSkill.objects.all()]
    })})


def projects(request):
    return render(request, 'projects.html', context={'data': dumps({
        'projects': [getSerializedProject(p) for p in ProjectView.getProjects()],
        'functions': [getSerializedProjectFunction(f) for f in ProjectFunction.objects.all()],
        'skills': [getSerializedProjectSkill(s) for s in ProjectSkill.objects.all()]
    })})


def termsOfService(request):
    return render(request, 'termsOfService.html', context={})


def _getUnauthorizedPage(request):
    # If the user is logged in, they are truly unauthorized
    if security.getSessionUser(request):
        return _getErrorPage(request, HTTPStatus.UNAUTHORIZED, 'You do not have permission to view this account')
    else:
        return render(request, 'login.html')


def _getErrorPage(request, errorStatus, errorMessage):
    return render(request, 'errors.html', {
        'data': dumps({'error': errorStatus, 'text': errorMessage})})
