from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .forms import ProfileUpdateForm
from .models import Profile
from feed.models import Tweet
from django.contrib import messages
from PIL import Image
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if(request.method == 'POST'):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Account created')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html',{'form':form})

@login_required
def profile(request):
    # user = User.objects.get(username=username)
    # profile = Profile.objects.get(user=user)
    # tweets = Tweet.objects.filter(user=user).order_by('-created_at')
    user = request.user
    profile= user.profile
    tweets = Tweet.objects.filter(user=user).order_by('-created_at')
    return render(request, 'accounts/profile.html',{'user': user, 'profile': profile, 'tweets': tweets})
    

 
def profileupdate(request):
    if(request.method == 'POST'):
       pform = ProfileUpdateForm(request.POST, request.FILES, instance= request.user.profile)
       if pform.is_valid():
            pform.save()
            return redirect('profile')
    else:
        pform = ProfileUpdateForm(instance= request.user.profile)
    return render(request, 'accounts/profileupdate.html', {'pform': pform})

@login_required
def SearchView(request):
    if request.method == 'POST':
        kerko = request.POST.get('search')
        print(kerko)
        results = User.objects.filter(username__contains=kerko)
        text = {
            'results':results
        }
        return render(request, 'accounts/search_result.html', text)