"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from djangoProject import settings
from posts import views
from posts.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='home'),
    re_path(r'^user/(\w+)/$', Profile.as_view(), name='profile'),
    re_path(r'^user/(\w+)/post/$', PostPost.as_view(), name='post'),
    re_path(r'^search/$', Search.as_view()),
    re_path(r'^search/hashtag$', SearchTag.as_view()),
    re_path(r'^hashtag.json', TagJson.as_view()),
    re_path(r'^login/$', LoginUser.as_view(), name='login'),
    re_path(r'^register/$', RegisterUser.as_view(), name='register'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('about/', about, name='about'),
    path('logout/', logout_user, name='logout')


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
