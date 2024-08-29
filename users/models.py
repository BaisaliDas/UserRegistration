from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import timedelta

from django.utils.crypto import get_random_string

# Create your models here.
class Profile(models.Model):
    profile_pic=models.ImageField(upload_to='PP')
    address=models.TextField()
    username=models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username.username
    
    