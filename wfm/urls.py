from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('process_ponctual_forecast/', views.process_ponctual_forecast, name="process_ponctual_forecast"),
    path('process_ponctual_reverse/', views.process_ponctual_reverse, name="process_ponctual_reverse"),
    path('auth/', views.auth, name="auth"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('download_template/', views.download_template)
]
