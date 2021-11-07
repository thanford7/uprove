from http import HTTPStatus
from json import dumps

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response

from .apis.user import UserView, UserProfileView


# Create your views here.
def homepage(request):
    return render(request, 'home.html', context={})


def about(request):
    return render(request, 'about.html', context={})


def accountSettings(request, userId):
    if not isPermittedSessionUser(request, userId):
        return render(request, 'errors.html', {'data': dumps({'error': HTTPStatus.UNAUTHORIZED, 'text': 'You do not have permission to view this account'})})
    user = UserView.getUser(userId)
    serializedUser = {}
    if user:
        serializedUser = UserView.serializeUser(user)
    return render(request, 'accountSettings.html', {'data': dumps(serializedUser)})


def contact(request):
    return render(request, 'contact.html', context={})


def errors(request):
    return render(request, 'errors.html', context={})


def privacy(request):
    return render(request, 'privacy.html', context={})


def profile(request, profileId):
    return render(request, 'userProfile.html', context={'data': UserProfileView.getUserProfile(profileId)})


def projects(request):
    return render(request, 'projects.html', context={})


def termsOfService(request):
    return render(request, 'termsOfService.html', context={})


def isPermittedSessionUser(request, userId):
    try:
        sessionUser = request.session['uproveUser']
        return sessionUser['id'] == userId
    except KeyError:
        return False
