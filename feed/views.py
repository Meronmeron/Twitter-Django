from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Tweet
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

def is_users(post_user, logged_user):
    return post_user == logged_user

class TweetListView(LoginRequiredMixin,ListView):
    model = Tweet
    template_name = 'feed/home.html'
    ordering = ['-created_at']


class TweetCreateView(LoginRequiredMixin,CreateView):
    model = Tweet

    fields = ['text']
    success_url = '/'
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Tweet
    template_name = 'feed/tweet_form.html'
    fields = ['text']
    success_url = '/'
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().user, self.request.user)


class TweetDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Tweet
    template_name = 'feed/tweet_confirm.html'
    success_url = '/'
    def test_func(self):
        return is_users(self.get_object().user, self.request.user)
   
    # def test_fun(self):
    #     tweet = self.get_object()
    #     if (self.request.user == tweet.user.username):
    #         return True
    #     return False

    

