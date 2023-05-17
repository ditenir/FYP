from math import exp

from main import get_service_level, erlang_c


def fin_maximum_calls_nelson(ag, aht, target, servicel):
    # a=call_intensity(calls_per_hour(calls,period,workh,unit),aht)

    i = ag - 1

    pw = erlang_c(i, ag)

    s = get_service_level(pw, ag, i, target, aht)

    # print(s,' ',i*3600/aht)

    while s < servicel:
        i = i - 1

        pw = erlang_c(i, ag)

        s = get_service_level(pw, ag, i, target, aht)

    # print(s,' ',i*3600/aht)

    return (
        i * 3600 / aht
    )  # i is the number of possible Erlangs so *3600/aht gives the number of calls


def fin_maximum_calls(ag, aht, target, servicel):
    # a=call_intensity(calls_per_hour(calls,period,workh,unit),aht)

    i = ag * 3600 / aht

    pw = erlang_c(i, ag)

    s = get_service_level(pw, ag, i, target, aht)

    # print(s,' ',i*3600/aht)

    while s < servicel:
        i = i - 1

        pw = erlang_c(i, ag)

        s = get_service_level(pw, ag, i, target, aht)

    # print(s,' ',i*3600/aht)

    return (
        i * 3600 / aht
    )  # i is the number of possible Erlangs so *3600/aht gives the number of calls


print(fin_maximum_calls(10, 180, 120, 90))
print(fin_maximum_calls_nelson(10, 180, 120, 90))
