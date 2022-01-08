import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import viewsets
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, FormView

from posts.forms import PostForm, SearchForm, SearchTagForm, LoginUserForm, RegisterUserForm, ContactForm, ProfileForm
from user_profile.models import User
from .models import Post, HashTag, DisLike
from .utils import DataMixin

menu = [{'title': "About website", 'url_name': 'about'},
        {'title': "FeedBack", 'url_name': 'contact'}
        ]


class Info(View):

    def get(self, request, username):
        user = User.objects.get(username=username)
        if request.user.is_authenticated:
            info = User.objects.all()
            context = {
                'user': user,
                'info': info
            }
            return render(request, 'info.html', context)
        else:
            return redirect('login')


class Index(View):

    def get(self, request):
        context = {'menu': menu, 'text': 'Hello world'}
        return render(request, 'base.html', context)


def about(request):
    contact_list = User.objects.all()
    return render(request, 'about.html', )


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Feedback")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class Profile(View):
    def get(self, request, username):
        likeAuthor = request.GET.get('name')
        id = request.GET.get('id')
        print(likeAuthor ,id)
        if likeAuthor and id:
            post = Post.objects.get(id=id)
            if not likeAuthor+',' in post.likesAuthors:
                print(1)
                authors = post.likesAuthors+likeAuthor+','
                likes = int(post.likesCount)+1
            else:
                print(2)
                authors = post.likesAuthors.replace(likeAuthor+',','')
                likes = int(post.likesCount)-1
            Post.objects.filter(id=id).update(likesAuthors=authors,likesCount=likes)

        likePosts = []
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user)
        for i in posts:
            if request.user.username+',' in i.likesAuthors:
                likePosts.append(i.id)

        # posts = Post.objects.all()
        form = PostForm()
        context = {
            'posts': posts,
            'user': user,
            'form': form,
            'likePosts':likePosts,
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


        context = {'tags': tags, 'searchtag': form, }
        return render(request, 'search_tags.html', context)


class TagJson(View):
    def get(self, request):
        q = request.GET.get('q', '')
        taglist = []
        tags = HashTag.objects.filter(name__icontains=q)
        for tag in tags:
            new = {'q': tag.name, 'count': int(len(tag.post.all()))}
            taglist.append(new)
        return HttpResponse(json.dumps(taglist), content_type="application/json")


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Authentication")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Registration")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')


def logout_user(request):
    logout(request)
    return redirect('login')


class UpdatePostVote(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):

        post_id = self.kwargs.get('post_id', None)
        opinion = self.kwargs.get('opinion', None)  # like or dislike button clicked

        post = get_object_or_404(Post, id=post_id)

        try:
            # If child DisLike model doesnot exit then create
            post.dis_likes
        except Post.dis_likes.RelatedObjectDoesNotExist as identifier:
            DisLike.objects.create(comment=post)

        try:
            # If child Like model doesnot exit then create
            post.likes
        except Post.likes.RelatedObjectDoesNotExist as identifier:
            Like.objects.create(comment=post)

        if opition.lower() == 'like':

            if request.user in post.likes.users.all():
                post.likes.users.remove(request.user)
            else:
                post.likes.users.add(request.user)
                post.dis_likes.users.remove(request.user)

        elif opition.lower() == 'dis_like':

            if request.user in post.dis_likes.users.all():
                post.dis_likes.users.remove(request.user)
            else:
                post.dis_likes.users.add(request.user)
                post.likes.users.remove(request.user)
        else:
            return HttpResponseRedirect(reverse('profile'))
        return HttpResponseRedirect(reverse('profile'))
