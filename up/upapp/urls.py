from django.urls import path

from . import views
from .apis import employer
from .apis import user

apiPath = 'api/v1/'

urlpatterns = [
    # Views
    path('', views.homepage, name='index'),
    path('privacy/', views.privacy, name='privacy'),
    path('user/<int:userId>/', views.user, name='user'),
    path('profile/<int:profileId>/', views.profile, name='profile'),

    # APIs
    path(apiPath + 'employer_interest/', employer.EmployerInterestView.as_view())
]
