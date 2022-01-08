from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from user_profile.models import User
from django.contrib.contenttypes.models import ContentType


# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='my_posts')
    text = models.CharField(max_length=300)
    likesCount = models.IntegerField(verbose_name='Лайки',default=0,null=0,blank=True)
    likesAuthors = models.TextField(null=0,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def get_total_likes(self):
        return self.likes.users.count()

    def get_total_dis_likes(self):
        return self.dis_likes.users.count()


class HashTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    post = models.ManyToManyField(Post)

    def __str__(self):
        return self.name


# class Like(models.Model):
#     ''' like  comment '''

#     post = models.OneToOneField(Post, related_name="likes", on_delete=models.CASCADE)
#     users = models.ManyToManyField(User, related_name='requirement_post_likes')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.post.comment)[:30]


class DisLike(models.Model):
    ''' Dislike  comment '''

    post = models.OneToOneField(Post, related_name="dis_likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_post_dis_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.post.comment)[:30]
