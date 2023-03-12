from .common import *


def calculate_ponctual_forecast(data):
    if data["aht_unit"] == "minutes":
        data["aht"] *= 60
    if data["max_waiting_time_unit"] == "minutes":
        data["max_waiting_time"] *= 60

    intensity = calls_per_hour(data) * data["aht"] / 3600
    raw_agent_number = find_optimal_raw_agent(data)
    optimal_agents_number = int(optimal_agent(data))
    raw_optimal_agents_number = optimal_agent_after_occupancy(data, raw_agent_number)
    service_level = get_service_level(
        erlang_c(intensity, round(raw_optimal_agents_number)),
        raw_optimal_agents_number,
        intensity,
        data["max_waiting_time"],
        data["aht"]
    )
    immediately_answered_calls = int(immediate_answered(
        erlang_c(intensity, int(raw_optimal_agents_number))
    ))
    average_speed_answered_calls = int(average_speed_answer(
        erlang_c(intensity, int(raw_optimal_agents_number)),
        data["aht"],
        raw_optimal_agents_number,
        intensity
    ))
    raw_agent_number = int(raw_agent_number)
    raw_optimal_agents_number = int(raw_optimal_agents_number)

    return {
        "raw_agent_number": raw_agent_number,
        "optimal_agents_number": optimal_agents_number,
        "raw_optimal_agents_number": raw_optimal_agents_number,
        "service_level": service_level,
        "immediately_answered_calls": immediately_answered_calls,
        "average_speed_answered_calls": average_speed_answered_calls,
    }
