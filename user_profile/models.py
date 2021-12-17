from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.

class User(AbstractBaseUser):
    login = models.CharField('username', max_length=25, unique=True, db_index=True)
    password = models.CharField('password', max_length=25)
    firstname = models.CharField('firstname', max_length=30)
    lastname = models.CharField('lastname', max_length=30)
    patronymic = models.CharField('patronymic', max_length=30)
    email = models.EmailField('email', max_length=30, unique=True)
    registration = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    country = models.CharField(max_length=30, default='Global')

    USERNAME_FIELD = 'login'

    def __init__(self):
        return self.login
