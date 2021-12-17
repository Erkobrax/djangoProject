from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
# Create your views here.
from django.views import View
from .models import Post, HashTag
from user_profile.models import User
from posts.forms import PostForm, SearchForm
from django.template.loader import render_to_string
import json


class Index(View):

    def get(self, request):
        context = {'text': 'Hello world'}
        return render(request, 'base.html', context)


class Profile(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user)
        form = PostForm()
        context = {
            'posts': posts,
            'user': user,
            'form': form,
        }
        return render(request, 'profile.html', context)


class PostPost(View):
    def post(self, request, username):
        form = PostForm(self.request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            post = Post(text=form.cleaned_data['text'], user=user)
            post.save()
            words = form.cleaned_data['text'].split(" ")
            for word in words:
                if word.startswith('#'):
                    hashtag, created = HashTag.objects.get_or_create(name=word)
                    hashtag.post.add(post)
        return HttpResponseRedirect('/user/' + username)


class Search(View):
    def get(self, request):
        form = SearchForm()
        context = {'search': form}
        return render(request, 'search.html', context)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['q']
            posts = Post.objects.filter(text__icontains=q)
            context = {'q': q, 'posts': posts}
            return_str = render_to_string('part_views/_post_search.html', context)
            return HttpResponse(json.dumps(return_str), content_type='application/json')
        else:
            HttpResponseRedirect('/search/')


class SearchTag(View):

    def get(self, request):
        form = SearchTagForm()
        context = {'searchtag': form}
        return render(request, 'search_tags.html', context)

    def post(self, request):
        q = request.POST['q']
        form = SearchTagForm()
        tags = HashTag.objects.filter(name__icontains=q)
        context = {'tags': tags, 'searchtag': form}
        return render(request, 'search_tags.html', context)
