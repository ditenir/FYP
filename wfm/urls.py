from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('process_ponctual_forecast/', views.process_ponctual_forecast, name="process_ponctual_forecast")
]
