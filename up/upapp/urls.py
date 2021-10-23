from django.urls import path

from . import views

app_name = 'upapp'
urlpatterns = [
    path('', views.homepage, name='index'),
    path('user/<int:userId>/', views.user, name='user'),
    path('profile/<int:profileId>/', views.profile, name='profile')
]
