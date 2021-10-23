from django.http import HttpResponse
from django.shortcuts import render

from .apis.user import UserView, UserProfileView

# Create your views here.`
def homepage(request):
    return render(request, 'home.html', context={})

def user(request, userId):
    return render(request, 'user.html', context=UserView.getUser(userId))

def profile(request, profileId):
    return render(request, 'userProfile.html', context=UserProfileView.getUserProfile(profileId))
