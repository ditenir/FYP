from django.contrib.auth import authenticate, login
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
    if user is not None:
        login(request, user)
    else:
        return render(request, 'wfm/auth.html')
    return redirect('index')


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

    result = calculate_ponctual_forecast(data)
    calculation = PonctualForecast.objects.create(
        user=request.user,
        required_agents_number=result["raw_agent_number"],
        agents_number_after_shrinkage=result["optimal_agents_number"],
        agents_number_max_occupancy=result["raw_optimal_agents_number"],
        service_level=result["service_level"],
        calls_without_delay=result["immediately_answered_calls"],
        average_speed=result["average_speed_answered_calls"]
    )
    return redirect('get_calculation', id=calculation.id)


@login_required
def process_ponctual_reverse(request):
    if request.FILES:
        dataframe = pd.read_excel(request.FILES['input_file'])
        data = {
            "agents_num": dataframe["Number of working agents"][0],
            "aht": dataframe["Average Handling Time"][0],
            "aht_unit": dataframe["Average Handling Time Unit"][0],
            "max_waiting_time": dataframe["Target maximum waiting time"][0],
            "max_waiting_time_unit": dataframe["Target maximum waiting time unit"][0],
            "service_level": dataframe["Desired maximum occupancy"][0],
            "occupancy": dataframe["Desired maximum occupancy"][0]
        }
    else:
        data = dict(request.POST)
        data["agents_num"] = int(data["agents_num"][0])
        data["aht"] = int(data["aht"][0])
        data["aht_unit"] = data["aht_unit"][0]
        data["max_waiting_time"] = int(data["max_waiting_time"][0])
        data["max_waiting_time_unit"] = data["max_waiting_time_unit"][0]
        data["service_level"] = int(data["service_level"][0])
        data["occupancy"] = int(data["occupancy"][0])

    result = calculate_ponctual_reverse(data)
    calculation = PunctualReverseForecast.objects.create(
        user=request.user,
        max_calls_number=result["max_calls_per_hour"],
        max_occupancy=result["max_occupancy"],
        max_calls_with_occupancy=result["max_calls"],
        average_occupancy=result["occupancy_level"],
        service_level=result["service_level"]
    )
    return redirect('get_calculation', id=calculation.id)


def process_multiple_period(request):
    dataframe = pd.read_excel(request.FILES['input_file'])
    data = dict(request.POST)
    data["calls_num"] = int(data["calls_num"][0])
    data["aht"] = int(data["aht"][0])
    data["aht_unit"] = data["aht_unit"][0]
    data["max_waiting_time"] = int(data["max_waiting_time"][0])
    data["max_waiting_time_unit"] = data["max_waiting_time_unit"][0]
    data["service_level"] = int(data["service_level"][0])
    data.pop('csrfmiddlewaretoken')
    result = calculate_multiple_period(dataframe, data)
    tables = []
    agents = []
    for i in result:
        tables.append(MultiplePeriodTable.objects.create(
            zone=i[0],
            language=i[1],
            media_type=i[2],
            agents_table=result[i]
        ))
        for j in result[i]:
            agents.append(sum(result[i][j]))
    calculation = MultiplePeriodForecast.objects.create(
        user=request.user,
        total_agents_number=sum(agents) / (len(agents) * 7)
    )
    calculation.agents_per_criteria.set(tables)
    return redirect('get_calculation', id=calculation.id)


def download_template(request):
    template = os.path.join(settings.EXCEL_TEMPLATES_DIRECTORY, f'input/{ request.GET.get("type")}.xlsx')
    file = open(template, 'rb')
    response = FileResponse(
        file,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f"inline; filename={ request.GET.get('type') }.xlsx"
    return response


def get_calculation(request, id):
    calculation = Calculation.objects.get(pk=id)
    if hasattr(calculation, "ponctualforecast"):
        return render(request, "wfm/ponctual_forecast_output.html", {
            "ponctual_forecast": calculation.ponctualforecast
        })
    elif hasattr(calculation, "punctualreverseforecast"):
        return render(request, "wfm/ponctual_reverse_output.html", {
            "punctual_reverse": calculation.punctualreverseforecast
        })
    elif hasattr(calculation, "multipleperiodforecast"):
        tables = []
        for i in calculation.multipleperiodforecast.agents_per_criteria.all():
            tables.append({
                "zone": i.zone,
                "language": i.language,
                "media_type": i.media_type,
                "agents_table": i.agents_table
            })
        return render(request, "wfm/multiple_period_output.html", {
            "agents_number": calculation.multipleperiodforecast.total_agents_number,
            "tables": tables
        })


def export_calculation(request, id):
    calculation = Calculation.objects.get(pk=id)
    if hasattr(calculation, "ponctualforecast"):
        export = open(ponctual_forecast_excel(calculation.ponctualforecast), "rb")
        response = FileResponse(
            export,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "inline; filename=export.xlsx"
        return response

    elif hasattr(calculation, "punctualreverseforecast"):
        export = open(ponctual_reverse_excel(calculation.punctualreverseforecast), "rb")
        response = FileResponse(
            export,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "inline; filename=export.xlsx"
        return response







