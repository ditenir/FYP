from math import exp
import random
import string


def calls_per_hour(data):
    """int,str,float->int
    This function returns calls per hour, calls are integer number of calls per period,
    period is a string, 'minute,hour,day,month,year', the unit defines how many periods
    the function returns the number of calls, unit is one by default per hour"""
    result = data["calls_num"] / data["period_num"]
    if data["period_type"] == "minute":
        result *= 60
    elif data["period_type"] != "hour":
        result /= data["working_hours_num"]
        if data["period_type"] == "month":
            result /= 30
        elif data["period_type"] == "year":
            result /= 365
    return result


def erlang_b(e, m):
    inv_b = 1.0
    for j in range(1, m + 1):
        inv_b = 1.0 + inv_b * (j / e)
    return 1.0 / inv_b


def avoid_big_fact(a, n):
    val = 1
    for i in range(1, n + 1):
        val = val * a / i
    return val


def erlang_c(a, n):
    """returns Erlang probability of a call waiting
    A is trafic intensity and N is number of available channels or agents"""
    l = avoid_big_fact(a, n) * (n / (n - a))
    sum_ = 0
    for i in range(n):
        sum_ += avoid_big_fact(a, i)
    return l / (sum_ + l)


def get_service_level(pw, agent_number, intensity, target, aht):
    """return the service quality in percentage
    pw is the erlangc probability, n is number of agents,a is intensity, target is waiting time
    in seconds and aht is average handling time in seconds"""
    a = 1 - (pw * exp(-(agent_number - intensity) * target / aht))
    return a * 100


def average_speed_answer(pw, aht, agent_number, intensity):
    """returns the average speed of answering pw is ErlangC, aht average handling time"""
    return (pw * aht) / (agent_number - intensity)


def immediate_answered(pw):
    """returns percentage answered imediTLY  pw is ErlangC"""
    return (1 - pw) * 100


def occupancy(intensity, agents):
    """returns occupancy of agents in percentage"""
    return (intensity / agents) * 100


def agent_after_shrinkage(sh, agents):
    """retuns number fo agents needed after counting shrinkage
    sh is the shrinkage in percentage for example 30  is for 30%"""
    return agents / (1 - sh / 100)


def find_optimal_raw_agent(data):
    """returns optimal number of agents for calls in period,workh
    is working hours in aday aht is average handling time,
    target is maximum waiting time, servicel is servicelevel percentage"""
    a = calls_per_hour(data) * data["aht"] / 3600
    i = int(a) + 1
    pw = erlang_c(a, i)
    s = get_service_level(pw, i, a, data["max_waiting_time"], data["aht"])
    while s < data["service_level"]:
        i = i + 1
        pw = erlang_c(a, i)
        s = get_service_level(pw, i, a, data["max_waiting_time"], data["aht"])
    return i


def optimal_agent(data):
    """returns optimal number of agents for calls in period,workh
    is working hours in aday aht is average handling time,
    target is maximum waiting time, servicel is servicelevel percentage,
    sh is shrinkage rate in percentage"""
    return agent_after_shrinkage(
        data["shrinkage"],
        find_optimal_raw_agent(data),
    )


def optimal_agent_after_occupancy(data, raw):
    """rises the agent number until the maximum occupancy, oc is met after shrinkage"""
    a = calls_per_hour(data) * data["aht"] / 3600
    oca = (a / raw) * 100

    while oca > data["max_occupancy"]:
        raw = raw + 1
        oca = (a / raw) * 100
    return agent_after_shrinkage(data["shrinkage"], raw)


def find_maximum_calls(data):
    i = data["agents_num"] - 1
    pw = erlang_c(i, data["agents_num"])
    s = get_service_level(pw, data["agents_num"], i, data["max_waiting_time"], data["aht"])
    while s < data["service_level"]:
        i = i - 1
        pw = erlang_c(i, data["agents_num"])
        s = get_service_level(pw, data["agents_num"], i, data["max_waiting_time"], data["aht"])
    return (
        i * 3600 / data["aht"]
    )  # i is the number of possible Erlangs so *3600/aht gives the number of calls


def generate_token():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(63))
