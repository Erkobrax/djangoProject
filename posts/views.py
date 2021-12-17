from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views import View
from .models import Post
from user_profile.models import User


class Index(View):

    def get(self, request):
        context = {'text': 'Hello world'}
        return render(request, 'base.html', context)


class Profile(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user)
        context = {
            'posts': posts,
            'user': user,
        }
        return render(request, 'profile.html', context)
