from http import HTTPStatus
from json import dumps

from django.shortcuts import render

from apis.employer import EmployerView
from apis.project import ProjectView
from modelSerializers import getSerializedProject, getSerializedEmployer, getSerializedUser
from . import security
from .apis.user import UserView, UserProfileView


# Create your views here.
def homepage(request):
    return render(request, 'home.html', context={})


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
        'users': [getSerializedUser(u) for u in UserView.getUsers()]
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
    return render(request, 'errors.html', {
        'data': dumps({'error': HTTPStatus.UNAUTHORIZED, 'text': 'You do not have permission to view this account'})})
