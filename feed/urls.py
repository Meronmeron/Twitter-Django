from django.urls import path
from . import views
from .models import Tweet
from .views import TweetListView,TweetCreateView,TweetUpdateView,TweetDeleteView,TweetDetailView,FollowersListView,FollowsListView,UserTweetListView



urlpatterns = [    
    path('',TweetListView.as_view(),name='home'),
    path('user/<str:username>', UserTweetListView.as_view(), name='user-tweets'),
    path('create/',TweetCreateView.as_view(),name='tweetcreate'),
    path('tweet/<int:pk>/update',TweetUpdateView.as_view(),name='tweetupdate'),
    path('tweet/<int:pk>/delete',TweetDeleteView.as_view(),name='tweetdelete'),
    path('tweet/<int:pk>/', TweetDetailView.as_view(), name='tweetdetail'),
    path('user/<str:username>/follows', FollowsListView.as_view(), name='user-follows'),
    path('user/<str:username>/followers', FollowersListView.as_view(), name='user-followers'),

]