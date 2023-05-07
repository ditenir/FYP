import os

from django.conf import settings
from openpyxl.reader.excel import load_workbook

from .common import *


def calculate_ponctual_reverse(data):
    if data["aht_unit"] == "minutes":
        data["aht"] *= 60
    if data["max_waiting_time_unit"] == "minutes":
        data["max_waiting_time"] *= 60

    max_calls_per_hour = find_maximum_calls(data)
    max_occupancy = occupancy(data["aht"] * max_calls_per_hour / 3600, data["agents_num"])
    occupancy_level = max_occupancy
    max_calls = max_calls_per_hour
    while occupancy_level > data["occupancy"]:
        max_calls -= 1
        occupancy_level = occupancy(data["aht"] * max_calls / 3600, data["agents_num"])
    service_level = int(get_service_level(
        erlang_c(data["aht"] * max_calls_per_hour / 3600, data["agents_num"]),
        data["agents_num"],
        data["aht"] * max_calls / 3600,
        data["max_waiting_time"],
        data["aht"]
    ))
    occupancy_level = int(occupancy_level)
    max_occupancy = int(max_occupancy)
    return {
        "max_calls_per_hour": max_calls_per_hour,
        "max_occupancy": max_occupancy,
        "max_calls": max_calls,
        "occupancy_level": occupancy_level,
        "service_level": service_level,
    }


def generate_excel(calculation):
    workbook = load_workbook(os.path.join(settings.EXCEL_TEMPLATES_DIRECTORY, "output/punctual_reverse.xlsx"))
    worksheet = workbook.active
    worksheet['A2'] = calculation.max_calls_number
    worksheet['B2'] = calculation.max_occupancy
    worksheet['C2'] = calculation.max_calls_with_occupancy
    worksheet['D2'] = calculation.average_occupancy
    worksheet['E2'] = calculation.service_level
    worksheet.views.sheetView[0].selection[0].activeCell = "A1"
    path = "/tmp/punctual_reverse.xlsx"
    workbook.save(path)
    return path
