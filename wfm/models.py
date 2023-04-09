from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Calculation(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PonctualForecast(Calculation):
    required_agents_number = models.IntegerField()
    agents_number_after_shrinkage = models.IntegerField()
    agents_number_max_occupancy = models.IntegerField()
    service_level = models.IntegerField()
    calls_without_delay = models.IntegerField()
    average_speed = models.IntegerField()


