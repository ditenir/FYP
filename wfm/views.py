from django.shortcuts import render
from .helpers import *


def index(request):
    return render(request, 'wfm/index.html')


def process_ponctual_forecast(request):
    data = dict(request.POST)
    data["calls_num"] = int(request.POST["calls_num"])
    data["period_num"] = int(request.POST["period_num"])
    data["working_hours_num"] = int(request.POST["working_hours_num"])
    data["aht"] = int(request.POST["aht"])
    data["max_waiting_time"] = int(request.POST["max_waiting_time"])
    data["service_level"] = int(request.POST["service_level"])
    data["shrinkage"] = int(request.POST["shrinkage"])
    data["max_occupancy"] = int(request.POST["max_occupancy"])
    data["period_type"] = data["period_type"][0]
    data["max_waiting_time_unit"] = data["max_waiting_time_unit"][0]
    data["aht_unit"] = data["aht_unit"][0]

    context = calculate_ponctual_forecast(data)
    return render(request, "wfm/ponctual_forecast_output.html", context)


