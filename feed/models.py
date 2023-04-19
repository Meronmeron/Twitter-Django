from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class Tweet(models.Model):
    text = models.CharField(max_length=140,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True)
