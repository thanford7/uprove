from django.urls import path, include

from . import views
from . import viewsAuth
from .apis import sendEmail
from .apis import user

apiPath = 'api/v1/'

urlpatterns = [
    # Views
    path('', views.homepage, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('profile/<int:profileId>/', views.profile, name='profile'),
    path('projects/', views.projects, name='projects'),
    path('terms-of-service/', views.termsOfService, name='termsOfService'),
    path('user/<int:userId>/', views.user, name='user'),

    # APIs

    # Email
    path(apiPath + 'email/', sendEmail.EmailView.as_view()),

    # Authentication
    path(apiPath + 'login/', viewsAuth.LoginView.as_view()),
]
