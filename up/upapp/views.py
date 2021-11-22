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
    if not security.isPermittedSessionUser(request, userId):
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
        'projects': [getSerializedProject(p) for p in ProjectView.getProjects()],
        # TODO: Lazy load employers and users since this will get long
        'employers': [getSerializedEmployer(e) for e in EmployerView.getEmployers()],
        'users': [getSerializedUser(u) for u in UserView.getUsers()],
        'functions': [getSerializedProjectFunction(f) for f in ProjectFunction.objects.all()],
        'skills': [getSerializedProjectSkill(s) for s in ProjectSkill.objects.all()]
    })})


def contact(request):
    return render(request, 'contact.html', context={})


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


def projects(request):
    return render(request, 'projects.html', context={})


def termsOfService(request):
    return render(request, 'termsOfService.html', context={})


def _getUnauthorizedPage(request):
    # If the use is logged in, they are truly unauthorized
    if security.getSessionUser(request):
        return render(request, 'errors.html', {
            'data': dumps({'error': HTTPStatus.UNAUTHORIZED, 'text': 'You do not have permission to view this account'})})
    else:
        return render(request, 'login.html')
