from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import Usermanager

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=20,unique=True)
    email = models.CharField(max_length=254)
    phone_num = models.CharField( max_length=12,unique=True)
    is_phone_verified = models.BooleanField(default=False)
    otp=models.CharField(max_length=6)

    USERNAME_FIELD= 'username'
    REQUIRED_FIELDS= []

    objects = Usermanager()