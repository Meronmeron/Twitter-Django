from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Tweet
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from accounts.models import Follow,Profile
def is_users(post_user, logged_user):
    return post_user == logged_user

class TweetListView(LoginRequiredMixin,ListView):
    model = Tweet
    template_name = 'feed/home.html'
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        qs = Follow.objects.filter(user=user)
        follows = [user]
        for obj in qs:
            follows.append(obj.follow_user)
        return Tweet.objects.filter(user__in=follows).order_by('-created_at')


class UserTweetListView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = 'feed/user_posts.html'
    context_object_name = 'tweets'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        visible_user = self.visible_user()
        logged_user = self.request.user
        print(logged_user.username == '', file=sys.stderr)

        if logged_user.username == '' or logged_user is None:
            can_follow = False
        else:
            can_follow = (Follow.objects.filter(user=logged_user,
                                                follow_user=visible_user).count() == 0)
        data = super().get_context_data(**kwargs)

        data['user_profile'] = visible_user
        data['can_follow'] = can_follow
        return data

    def get_queryset(self):
        user = self.visible_user()
        return Tweet.objects.filter(user=user).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        if request.user.id is not None:
            follows_between = Follow.objects.filter(user=request.user,
                                                    follow_user=self.visible_user())

            if 'follow' in request.POST:
                    new_relation = Follow(user=request.user, follow_user=self.visible_user())
                    if follows_between.count() == 0:
                        new_relation.save()
            elif 'unfollow' in request.POST:
                    if follows_between.count() > 0:
                        follows_between.delete()

        return self.get(self, request, *args, **kwargs)





class TweetCreateView(LoginRequiredMixin,CreateView):
    model = Tweet
    template_name = 'feed/create.html'
    fields = ['text']
    success_url = '/'
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add a new Tweet'
        return data

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


class TweetDetailView(DetailView):
    model = Tweet
    template_name = 'feed/tweet_detail.html'
    context_object_name = 'tweets'

    def test_func(self):
        return is_users(self.get_object().user, self.request.user)

class FollowsListView(ListView):
    model = Follow
    template_name = 'feed/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'follows'
        return data


class FollowersListView(ListView):
    model = Follow
    template_name = 'feed/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(follow_user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'followers'
        return data



    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     # comments_connected = Comment.objects.filter(post_connected=self.get_object()).order_by('-date_posted')
    #     # data['comments'] = comments_connected
    #     data['form'] = NewCommentForm(instance=self.request.user)
    #     return data

    # def tweet(self, request, *args, **kwargs):
    #     new_comment = Comment(content=request.POST.get('content'),
    #                           author=self.request.user,
    #                           post_connected=self.get_object())
    #     new_comment.save()

    #     return self.get(self, request, *args, **kwargs)  
    # def test_fun(self):
    #     tweet = self.get_object()
    #     if (self.request.user == tweet.user.username):
    #         return True
    #     return False

    

