from django.shortcuts import render
from .helpers import *


def index(request):
    return render(request, 'wfm/index.html')


def process_ponctual_forecast(request):
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

