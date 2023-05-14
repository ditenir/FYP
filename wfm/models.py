from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Calculation(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=31, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PonctualForecast(Calculation):
    required_agents_number = models.IntegerField()
    agents_number_after_shrinkage = models.IntegerField()
    agents_number_max_occupancy = models.IntegerField()
    service_level = models.IntegerField()
    calls_without_delay = models.IntegerField()
    average_speed = models.IntegerField()


class PunctualReverseForecast(Calculation):
    max_calls_number = models.IntegerField()
    max_occupancy = models.IntegerField()
    max_calls_with_occupancy = models.IntegerField()
    average_occupancy = models.IntegerField()
    service_level = models.IntegerField()


class MultiplePeriodForecast(Calculation):
    total_agents_number = models.IntegerField()
    agents_per_criteria = models.ManyToManyField("MultiplePeriodTable")


class MultiplePeriodTable(models.Model):
    zone = models.CharField(max_length=63, null=True)
    language = models.CharField(max_length=15, null=True)
    media_type = models.CharField(max_length=15, null=True)
    agents_table = models.JSONField()
