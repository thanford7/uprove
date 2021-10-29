from django.urls import path

from . import views
from .apis import employer, sendEmail
from .apis import user

apiPath = 'api/v1/'

urlpatterns = [
    # Views
    path('', views.homepage, name='index'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms-of-service/', views.termsOfService, name='termsOfService'),
    path('contact/', views.contact, name='contact'),
    path('user/<int:userId>/', views.user, name='user'),
    path('profile/<int:profileId>/', views.profile, name='profile'),

    # APIs
    path(apiPath + 'employer_interest/', employer.EmployerInterestView.as_view()),

    # Email
    path(apiPath + 'email/', sendEmail.EmailView.as_view())
]
