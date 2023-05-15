from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('process_ponctual_forecast/', views.process_ponctual_forecast, name="process_ponctual_forecast"),
    path('process_ponctual_reverse/', views.process_ponctual_reverse, name="process_ponctual_reverse"),
    path('process_multiple_period/', views.process_multiple_period, name="process_multiple_period"),
    path('auth/', views.auth, name="auth"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.sign_out, name="logout"),
    path('request_reset_password', views.request_reset_password, name='request_reset_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('download_template/', views.download_template),
    path('calculations/<int:id>/', views.get_calculation, name="get_calculation"),
    path('calculations/<int:id>/export/', views.export_calculation, name="export_calculation"),
    path('calculations/<int:id>/delete/', views.delete_calculation, name="delete_calculation"),
    path('history/', views.history, name="history"),
    path('punctual_forecast/', views.punctual_forecast, name="punctual_forecast"),
    path('punctual_reverse/', views.punctual_reverse, name="punctual_reverse"),
    path('multiple_period/', views.multiple_period, name="multiple_period"),
]
