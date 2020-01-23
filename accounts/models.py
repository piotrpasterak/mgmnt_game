from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import check_password as ckpass,\
    make_password as mkpass, is_password_usable as ispassuse


class CustomUser(AbstractUser):
    password = models.CharField(max_length=127)
    email = models.CharField(max_length=255)
    gender = models.CharField(max_length=7)
    experience = models.IntegerField(default=0)

