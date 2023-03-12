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
