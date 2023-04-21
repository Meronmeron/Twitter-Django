from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Tweet(models.Model):
    text = models.TextField(max_length=140, default = '')
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


