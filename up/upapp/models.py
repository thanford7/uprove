from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=75)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profilePicture = models.ImageField(upload_to='uploads/')
