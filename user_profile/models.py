from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('username', max_length=25, unique=True, db_index=True)
    password = models.CharField('password1', max_length=25)
    password2 = models.CharField('password2', max_length=25, default='SOME STRING')
    firstname = models.CharField('firstname', max_length=30)
    lastname = models.CharField('lastname', max_length=30)
    patronymic = models.CharField('patronymic', max_length=30)
    email = models.EmailField('email', max_length=30, unique=True)
    registration = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    country = models.CharField('country', max_length=30, default='Global')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
