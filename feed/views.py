from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Tweet
from .forms import TweetForm


@login_required
def home(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'feed/home.html', {'tweets': tweets})


@login_required
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('home')
    else:
        form = TweetForm()
    return render(request, 'feed/create_tweet.html', {'form': form})


