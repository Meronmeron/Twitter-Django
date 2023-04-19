from django.urls import path
from . import views
from .models import Tweet


urlpatterns = [    
    path('',views.home, name='home'),
    path('profile/',views.profile, name='profile'),
    path('create_tweet/',views.create_tweet, name='create_tweet')
]