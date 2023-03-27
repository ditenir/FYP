from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.conf import settings
import os
import pandas as pd
from .models import *
from .helpers import *


def auth(request):
    return render(request, 'wfm/auth.html')


def signup(request):
    user = User.objects.create_user(
        request.POST["username"],
        request.POST["email"],
        request.POST["password"],
        first_name=request.POST["name"],
    )
    authenticate(request, username=user.username, password=request.POST["password"])
    return render(request, 'wfm/index.html', {'user': user})


def signin(request):
    user = authenticate(
        request,
        username=request.POST["username"],
        password=request.POST["password"]
    )
    return render(request, 'wfm/index.html', {'user': user})


@login_required
def index(request):
    return render(request, 'wfm/index.html', {'user': request.user})


@login_required
def process_ponctual_forecast(request):
    if request.FILES:
        dataframe = pd.read_excel(request.FILES['input_file'])
        data = {
            "calls_num": dataframe["Number of calls"][0],
            "period_num": dataframe["Period"][0],
            "period_type": dataframe["Period Unit"][0],
            "working_hours_num": dataframe["Number of working hours"][0],
            "aht": dataframe["Average Handling TIme"][0],
            "aht_unit": dataframe["Average handling time unit"][0],
            "max_waiting_time": dataframe["Target maximum waiting time"][0],
            "max_waiting_time_unit": dataframe["Target maximum waiting time unit"][0],
            "service_level": dataframe["Desired service level"][0],
            "shrinkage": dataframe["Shrinkage"][0],
            "max_occupancy": dataframe["Desired maximum occupancy"][0]
        }
    else:
        data = dict(request.POST)
        data["calls_num"] = int(data["calls_num"][0])
        data["period_num"] = int(data["period_num"][0])
        data["working_hours_num"] = int(data["working_hours_num"][0])
        data["aht"] = int(data["aht"][0])
        data["max_waiting_time"] = int(data["max_waiting_time"][0])
        data["service_level"] = int(data["service_level"][0])
        data["shrinkage"] = int(data["shrinkage"][0])
        data["max_occupancy"] = int(data["max_occupancy"][0])
        data["period_type"] = data["period_type"][0]
        data["max_waiting_time_unit"] = data["max_waiting_time_unit"][0]
        data["aht_unit"] = data["aht_unit"][0]

    context = calculate_ponctual_forecast(data)
    return render(request, "wfm/ponctual_forecast_output.html", context)


@login_required
def process_ponctual_reverse(request):
    data = dict(request.POST)
    print(data)
    data["agents_num"] = int(data["agents_num"][0])
    data["aht"] = int(data["aht"][0])
    data["aht_unit"] = data["aht_unit"][0]
    data["max_waiting_time"] = int(data["max_waiting_time"][0])
    data["max_waiting_time_unit"] = data["max_waiting_time_unit"][0]
    data["service_level"] = int(data["service_level"][0])
    data["occupancy"] = int(data["occupancy"][0])

    context = calculate_ponctual_reverse(data)
    return render(request, "wfm/ponctual_reverse_output.html", context)


def download_template(request):
    template = os.path.join(settings.EXCEL_TEMPLATES_DIRECTORY, f'input/{ request.GET.get("type")}.xlsx')
    file = open(template, 'rb')
    response = FileResponse(
        file,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "inline; filename=ponctual_forecast.xlsx"
    return response



