from django.urls import path
from . import views
from .models import Tweet


urlpatterns = [    
    path('',views.home, name='home'),
    path('create_tweet/',views.create_tweet, name='create_tweet')
]