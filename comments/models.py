from django.db import models
from user_profile.models import User
from posts.models import Post


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_favourite = models.BooleanField(default=False)


    def __str__(self):
        return self.text
