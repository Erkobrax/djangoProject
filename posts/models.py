from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from user_profile.models import User
from django.contrib.contenttypes.models import ContentType


# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='my_posts')
    text = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class HashTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    post = models.ManyToManyField(Post)

    def __str__(self):
        return self.name
