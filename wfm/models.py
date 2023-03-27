from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Calculation(models.Model):
    created_at = models.DateTimeField(auto_now=True)

