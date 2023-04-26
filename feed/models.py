from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Tweet(models.Model):
    text = models.TextField(max_length=140, default = '')
    image = models.ImageField(null=True, blank=True, upload_to='image_tweets')
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url 
        else:
            return "" 

