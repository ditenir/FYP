import PySimpleGUI as sg
from math import exp
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt


def calls_per_hour(calls, period, working_hours_day, unit=1):
    """int,str,float->int
    This function returns calls per hour, calls are integer number of calls per period,
    period is a string, 'minute,hour,day,month,year', the unit defines how many periods
    the function returns the number of calls, unit is one by default per hour"""
    if period == "minute":
        return calls * 60 / unit
    elif period == "hour":
        return calls / unit
    elif period == "day":
        return (calls / unit) / working_hours_day
    elif period == "month":
        return ((calls / 30) / working_hours_day) / unit
    elif period == "year":
        return ((calls / 365) / working_hours_day) / unit


def call_intensity(calls, aht):
    """int,float->int
    returns the number of Erlangs using call number per hour and the average handling time
     aht is given in seconds"""
    return calls * aht / 3600


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


def find_optimal_raw_agent(
    calls, period, unit, working_hours, aht, target, service_level
):
    """returns optimal number of agents for calls in period,workh
    is working hours in aday aht is average handling time,
    target is maximum waiting time, servicel is servicelevel percentage"""
    a = call_intensity(calls_per_hour(calls, period, working_hours, unit), aht)
    i = int(a) + 1
    pw = erlang_c(a, i)
    s = get_service_level(pw, i, a, target, aht)
    while s < service_level:
        i = i + 1
        pw = erlang_c(a, i)
        s = get_service_level(pw, i, a, target, aht)
    return i


def optimal_agent(calls, period, unit, working_hours, aht, target, service_level, sh):
    """returns optimal number of agents for calls in period,workh
    is working hours in aday aht is average handling time,
    target is maximum waiting time, servicel is servicelevel percentage,
    sh is shrinkage rate in percentage"""
    return agent_after_shrinkage(
        sh,
        find_optimal_raw_agent(
            calls, period, unit, working_hours, aht, target, service_level
        ),
    )


def optimal_agent_after_occupancy(oc, calls, period, working_hours, unit, aht, sh, raw):
    """rises the agent number until the maximum occupancy, oc is met after shrinkage"""
    a = call_intensity(calls_per_hour(calls, period, working_hours, unit), aht)
    oca = (a / raw) * 100

    while oca > oc:
        raw = raw + 1
        oca = (a / raw) * 100
    return agent_after_shrinkage(sh, raw)


def fin_maximum_calls(ag, aht, target, servicel):
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


sg.set_options(font="_ 10")


def windowtable(data, header):
    window = sg.Window(
        "Your Simulation so Far",
        [
            [
                sg.Table(
                    values=data,
                    headings=header,
                    max_col_width=13,
                    auto_size_columns=False,
                    justification="right",
                    # alternating_row_color='lightblue',
                    num_rows=min(len(data), 20),
                )
            ]
        ],
        finalize=True,
        location=(window2.current_location()[0], window2.current_location()[1] + 350),
    )

    return window


def window1open(val):
    window1 = sg.Window(
        "Results and shrinkage",
        [
            [sg.T("Your raw agents is " + str(val), size=(30, 1), k="-T-")],
            [sg.T("What is your Shrinkage", enable_events=True, k="-text2-")],
            [sg.I(k="-1input2-")],
            [
                sg.T(
                    "What is your maximum occupancy desired?",
                    enable_events=True,
                    k="-text3-",
                )
            ],
            [sg.I(k="-1input3-")],
            [
                sg.B("submit", k="-C-"),
                sg.B("View Search", key="view"),
                sg.B("Export to excel", key="export"),
                sg.B("Exit"),
            ],
        ],
        finalize=True,
        location=(
            window2.current_location()[0] + 350,
            window2.current_location()[1] + 50,
        ),
    )

    return window1


def windowrevopen(val):
    window1 = sg.Window(
        "Find maximum calls",
        [
            [sg.T("What is your agent number", enable_events=True, k="-text2-")],
            [sg.I(k="2input2")],
            [sg.T("What is your AHT in seconds?", enable_events=True, k="-text3-")],
            [sg.I(k="2input3")],
            [
                sg.T(
                    "Target maximum waiting time in seconds?",
                    enable_events=True,
                    k="-text5-",
                )
            ],
            [sg.I(k="2input4")],
            [
                sg.T(
                    "Desired service level in percentage?",
                    enable_events=True,
                    k="-text6-",
                )
            ],
            [sg.I(k="2input5")],
            [
                sg.T(
                    "What is your maximum desired occupancy in percentage\nFOR raw leave 100",
                    enable_events=True,
                    k="-text7-",
                )
            ],
            [sg.I(k="2input6", default_text="100")],
            [
                sg.B("submit", k="-Cr-"),
                sg.B("View Search", key="viewr"),
                sg.B("Export to excel", key="exportr"),
                sg.B("Exit"),
            ],
        ],
        finalize=True,
        location=(
            window2.current_location()[0] + 350,
            window2.current_location()[1] + 50,
        ),
    )

    return window1


def window2open():
    window2 = sg.Window(
        "Model Calculator-Powered by WFM Team",
        [
            [sg.B("I want Reverse calculation", k="-Rev-", font=("Arial", 14))],
            [sg.B("Forward -> fill below", font=("Arial", 12))],
            [sg.T("Number of calls", k="-T-", size=(37, 1))],
            [sg.I(size=(30, 1), k="-input1-")],
            [sg.T("in which period")],
            [
                sg.Combo(
                    values=("minute", "hour", "day", "month", "year"),
                    readonly=True,
                    enable_events=True,
                    k="-COMBO-",
                )
            ],
            [sg.T("How many periods?", enable_events=True, k="-text2-")],
            [sg.I(k="-input2-")],
            [sg.T("how many working hours a day?", enable_events=True, k="-text3-")],
            [sg.I(k="-input3-")],
            [sg.T("average handle time in seconds?", enable_events=True, k="-text4-")],
            [sg.I(k="-input4-")],
            [
                sg.T(
                    "Target maximum waiting time in seconds?",
                    enable_events=True,
                    k="-text5-",
                )
            ],
            [sg.I(k="-input5-")],
            [
                sg.T(
                    "Desired service level in percentage?",
                    enable_events=True,
                    k="-text6-",
                )
            ],
            [sg.I(k="-input6-")],
            [sg.B("submit", k="-B-"), sg.B("Exit")],
        ],
        finalize=True,
        location=(100, 70),
        size=(400, 500),
    )

    return window2


sg.theme("SystemDefaultForReal")

today = datetime.now()

fixed = datetime.strptime("2023-2-28 9:00:00", "%Y-%m-%d %H:%M:%S")

delta = today - fixed

maxtime = timedelta(days=40)

if delta > maxtime:

    sg.popup_auto_close("Please check for update", auto_close_duration=10)

else:

    menu_def = [
        [
            "&Simulation",
            [
                "&Ponctual forecast",
                "&Multiple period forecast",
                "&Multiple Language-period forecast",
                "&What if forecast",
            ],
        ],
        ["&Help", ["&import-file formats", "&How to use what if"]],
    ]

    mainwindow = sg.Window(
        "Multi-channel WF-Modeling",
        [
            [sg.Menu(menu_def, key="meuu")],
            [
                sg.Graph(
                    canvas_size=(400, 400),
                    graph_bottom_left=(0, 0),
                    graph_top_right=(400, 400),
                    background_color="Black",
                    key="graph",
                    enable_events=True,
                    drag_submits="enabled",
                )
            ],
            [sg.B("submit", k="-B-"), sg.B("View Graph"), sg.B("Exit")],
        ],
        finalize=True,
        location=(10, 10),
    )

    df = pd.DataFrame(
        columns=[
            "Time-Period Label",
            "Language",
            "Channel",
            "Number of calls",
            "calls in period",
            "number od periods",
            "working hours a day",
            "AHT",
            "Targetted max waiting time",
            "Service level",
            "shrinkage",
            "maximum occupancy desired",
            "Raw agent necessary",
            "agents after shrinkage",
            "agents after mac occupancy",
            "servicelevel acheived",
            "calls with no delay answered",
            "Average speed of answering",
            "occupancy",
        ]
    )

    df1 = pd.DataFrame(
        columns=[
            "Number of Agents",
            "AHT",
            "Targetted max waiting time",
            "Service level",
            "Your possible calls",
            "your occupancy",
            "Your possible calls after occ correction",
            "final occupancy",
            "Service acheived",
        ]
    )

    window1 = None

    window2 = None

    window3 = None

    win2 = False

    win3 = False

    win4 = False

    multilp = False

    while True:  # Event Loop

        lisa = []

        lisb = []

        window, event, values = sg.read_all_windows(timeout=100)

        if event == sg.WIN_CLOSED:

            if window == mainwindow:
                mainwindow.close()

                break

            if window == window1:
                window1.close()

            if window == window2:
                window2.close()

                win2 = False

            if win3:

                if window == window3:
                    window3.close()

                    win3 = False

            if win4:

                if window == windowrev:
                    windowrev.close()

                    win4 = False

        if event == "Ponctual forecast":
            multilp = False

            window2 = window2open()

        if event == "Multiple Language-period forecast":
            multilp = True

            text = sg.popup_get_file(
                "Load your Multiple period-Language volume file",
                default_extension="xlsx",
            )

            dfm = pd.read_excel(text, header=0)

            print(dfm)

            window2 = window2open()

            window2.Element("-input1-").Update(1, disabled=True, visible=False)

            window2.Element("-COMBO-").Update("minute", disabled=True, visible=False)

            window2.Element("-input2-").Update("1", disabled=True, visible=False)

            window2.Element("-input3-").Update("1", disabled=True, visible=False)

        if event == "Exit":

            mainwindow.close()

            if window1:
                window1.close()

            if window2:
                window2.close()

            if win3:

                if window3:
                    window3.close()

            if win4:

                if windowrev:
                    windowrev.close()

            sg.popup_auto_close("Exiting...")

            break

        if event == "-COMBO-":
            window.Element("-text2-").Update("how many " + values["-COMBO-"] + "s")

        if event == "-Rev-":

            if win4 == False:
                windowrev = windowrevopen(5)

                events, values = windowrev.read(timeout=10)

                win4 = True

        if event == "-Cr-":

            ag = int(values["2input2"])

            e = int(values["2input3"])

            f = int(values["2input4"])

            g = int(values["2input5"])

            r = int(values["2input6"])

            maxcalls = fin_maximum_calls(ag, e, f, g)

            occ = occupancy(e * maxcalls / 3600, ag)

            occ1 = occ

            maxcaloc = maxcalls

            while occ1 > r:
                maxcaloc = maxcaloc - 1

                occ1 = occupancy(e * maxcaloc / 3600, ag)

            sl = int(
                get_service_level(
                    erlang_c(e * maxcalls / 3600, ag), ag, e * maxcaloc / 3600, f, e
                )
            )

            occ1 = int(occ1)

            occ = int(occ)

            sg.popup(
                "Maximum calls in one hour = "
                + str(maxcalls)
                + "\n Your max occupancy is now = "
                + str(occ)
                + "%\n",
                "Applying your maximum occupancy\n now your maximum calls are="
                + str(maxcaloc)
                + "\n and your occupancy is= ",
                str(occ1) + "%\n" + "your service will be " + str(sl) + "%",
            )

            lisb.extend([ag, e, f, g, maxcalls, occ, maxcaloc, occ1, sl])

            a_series = pd.Series(lisb, index=df1.columns)

            df1 = df1.append(a_series, ignore_index=True)

        if event == "exportr":
            text = sg.popup_get_file(
                "Click on save as to browse", save_as=True, default_extension="xlsx"
            )

            df1.to_excel(text, index=False)

        if event == "viewr":

            if not win3:

                window3 = windowtable(df1.values.tolist(), df1.columns.tolist())

                win3 = True

            else:

                window3.close()

                window3 = windowtable(list(df1.values), list(df1.columns))

        if event == "-B-":

            if not win2:
                a = int(values["-input1-"])

                b = values["-COMBO-"]

                c = int(values["-input2-"])

                d = int(values["-input3-"])

                e = int(values["-input4-"])

                f = int(values["-input5-"])

                g = int(values["-input6-"])

                rawnumb = find_optimal_raw_agent(a, b, c, d, e, f, g)

                window1 = window1open(rawnumb)

                win2 = True

            else:

                a = int(values["-input1-"])

                b = values["-COMBO-"]

                c = int(values["-input2-"])

                d = int(values["-input3-"])

                e = int(values["-input4-"])

                f = int(values["-input5-"])

                g = int(values["-input6-"])

                events, values = window1.read(timeout=10)

                i = int(values["-1input2-"])

                x = int(values["-1input3-"])
                intensity = call_intensity(calls_per_hour(a, b, d, c), e)

                rawnumb = find_optimal_raw_agent(a, b, c, d, e, f, g)

                numba = optimal_agent(a, b, c, d, e, f, g, i)

                raw = optimal_agent_after_occupancy(x, a, b, d, c, e, i, rawnumb)

                occ = occupancy(intensity, raw)

                sl = get_service_level(
                    erlang_c(intensity, round(raw)), raw, intensity, f, e
                )

                call0 = immediate_answered(erlang_c(intensity, int(raw)))

                asa = average_speed_answer(
                    erlang_c(intensity, int(raw)), e, raw, intensity
                )

                asa = int(asa)

                rawnumb = int(rawnumb)

                numba = int(numba)

                raw = int(raw)

                call0 = int(call0)

                if multilp == False:

                    ln = None

                    ch = None

                    tm = None

                    lisa.extend(
                        [
                            tm,
                            ln,
                            ch,
                            a,
                            b,
                            c,
                            d,
                            e,
                            f,
                            g,
                            i,
                            x,
                            rawnumb,
                            numba,
                            raw,
                            sl,
                            call0,
                            asa,
                            occ,
                        ]
                    )

                    a_series = pd.Series(lisa, index=df.columns)

                    df = df.append(a_series, ignore_index=True)

                    sg.popup(
                        "your raw agent number is "
                        + str(rawnumb)
                        + "\n"
                        + " your agent number after shrinkage is "
                        + str(numba)
                        + "\n"
                        + "your agent number considering maximum occupancy is "
                        + str(raw)
                        + "\n"
                        + "your stats are: \nservice level is "
                        + str(sl)
                        + "\nyour percentage of calls answered with no delay is "
                        + str(call0)
                        + "\nyour average speed of answering is "
                        + str(asa)
                        + " seconds\n",
                        "Your occupancy is " + str(round(occ, 2)),
                    )

                else:

                    lanlist = dfm.columns.tolist()

                    timelist = dfm["Time-Period Label"].values.tolist()

                    channel = dfm["Channel"].values.tolist()

                    for ln in lanlist[3:]:

                        for ii in range(len(timelist)):
                            lisa = []

                            a = dfm[ln].values.tolist()

                            minutes = dfm["Minutes in Time-Period"].values.tolist()

                            b = "minute"

                            c = minutes[ii]

                            d = 1

                            tm = timelist[ii]

                            ch = channel[ii]

                            intensity = call_intensity(calls_per_hour(a, b, d, c), e)

                            rawnumb = find_optimal_raw_agent(a, b, c, d, e, f, g)

                            numba = optimal_agent(a, b, c, d, e, f, g, i)

                            raw = optimal_agent_after_occupancy(
                                x, a, b, d, c, e, i, rawnumb
                            )

                            occ = occupancy(intensity, raw)

                            sl = get_service_level(
                                erlang_c(intensity, round(raw)), raw, intensity, f, e
                            )

                            call0 = immediate_answered(erlang_c(intensity, int(raw)))

                            asa = average_speed_answer(
                                erlang_c(intensity, int(raw)), e, raw, intensity
                            )

                            asa = int(asa)

                            rawnumb = int(rawnumb)

                            numba = int(numba)

                            raw = int(raw)

                            call0 = int(call0)

                            lisa.extend(
                                [
                                    tm,
                                    ln,
                                    ch,
                                    a,
                                    b,
                                    c,
                                    d,
                                    e,
                                    f,
                                    g,
                                    i,
                                    x,
                                    rawnumb,
                                    numba,
                                    raw,
                                    sl,
                                    call0,
                                    asa,
                                    occ,
                                ]
                            )

                            a_series = pd.Series(lisa, index=df.columns)

                            df = df.append(a_series, ignore_index=True)

        if event == "-C-":

            i = int(values["-1input2-"])

            x = int(values["-1input3-"])

            events, values = window2.read(timeout=10)

            a = int(values["-input1-"])

            b = values["-COMBO-"]

            c = int(values["-input2-"])

            d = int(values["-input3-"])

            e = int(values["-input4-"])

            f = int(values["-input5-"])

            g = int(values["-input6-"])

            intensity = call_intensity(calls_per_hour(a, b, d, c), e)

            rawnumb = find_optimal_raw_agent(a, b, c, d, e, f, g)

            numba = optimal_agent(a, b, c, d, e, f, g, i)

            raw = optimal_agent_after_occupancy(x, a, b, d, c, e, i, rawnumb)

            occ = occupancy(intensity, raw)

            sl = get_service_level(erlang_c(intensity, round(raw)), raw, intensity, f, e)

            call0 = immediate_answered(erlang_c(intensity, int(raw)))

            asa = average_speed_answer(erlang_c(intensity, int(raw)), e, raw, intensity)

            asa = int(asa)

            rawnumb = int(rawnumb)

            numba = int(numba)

            raw = int(raw)

            call0 = int(call0)

            if multilp == False:

                ln = None

                ch = None

                tm = None

                lisa.extend(
                    [
                        tm,
                        ln,
                        ch,
                        a,
                        b,
                        c,
                        d,
                        e,
                        f,
                        g,
                        i,
                        x,
                        rawnumb,
                        numba,
                        raw,
                        sl,
                        call0,
                        asa,
                        occ,
                    ]
                )

                a_series = pd.Series(lisa, index=df.columns)

                df = df.append(a_series, ignore_index=True)

                sg.popup(
                    "your raw agent number is "
                    + str(rawnumb)
                    + "\n"
                    + " your agent number after shrinkage is "
                    + str(numba)
                    + "\n"
                    + "your agent number considering maximum occupancy is "
                    + str(raw)
                    + "\n"
                    + "your stats are: \nservice level is "
                    + str(sl)
                    + "\nyour percentage of calls answered with no delay is "
                    + str(call0)
                    + "\nyour average speed of answering is "
                    + str(asa)
                    + " seconds"
                )

            else:

                lanlist = dfm.columns.tolist()

                timelist = dfm["Time-Period Label"].values.tolist()

                channel = dfm["Channel"].values.tolist()

                for ln in lanlist[3:]:

                    for ii in range(len(timelist)):
                        lisa = []

                        a = dfm[ln].values.tolist()[ii]

                        minutes = dfm["Minutes in Time-Period"].values.tolist()

                        b = "minute"

                        c = minutes[ii]

                        d = 1

                        tm = timelist[ii]

                        ch = channel[ii]

                        intensity = call_intensity(calls_per_hour(a, b, d, c), e)

                        rawnumb = find_optimal_raw_agent(a, b, c, d, e, f, g)

                        numba = optimal_agent(a, b, c, d, e, f, g, i)

                        raw = optimal_agent_after_occupancy(
                            x, a, b, d, c, e, i, rawnumb
                        )

                        occ = occupancy(intensity, raw)

                        sl = get_service_level(
                            erlang_c(intensity, round(raw)), raw, intensity, f, e
                        )

                        call0 = immediate_answered(erlang_c(intensity, int(raw)))

                        asa = average_speed_answer(
                            erlang_c(intensity, int(raw)), e, raw, intensity
                        )

                        asa = int(asa)

                        rawnumb = int(rawnumb)

                        numba = int(numba)

                        raw = int(raw)

                        call0 = int(call0)

                        print("ln    ", ln)

                        lisa.extend(
                            [
                                tm,
                                ln,
                                ch,
                                a,
                                b,
                                c,
                                d,
                                e,
                                f,
                                g,
                                i,
                                x,
                                rawnumb,
                                numba,
                                raw,
                                sl,
                                call0,
                                asa,
                                occ,
                            ]
                        )

                        a_series = pd.Series(lisa, index=df.columns)

                        df = df.append(a_series, ignore_index=True)

        if event == "export":
            text = sg.popup_get_file(
                "Click on save as to browse", save_as=True, default_extension="xlsx"
            )

            df.to_excel(text, index=False)

        if event == "View Graph":
            if multilp:

                fig, ax = plt.subplots()

                for ln in lanlist[3:]:
                    print(ln)

                    ax.plot(
                        timelist,
                        df[df["Language"] == ln]["Raw agent necessary"],
                        label=ln,
                    )  # latex format

                    ax.legend(loc=0)

                    ax.set_xlabel("Time period", fontsize=18)

                    ax.set_ylabel("Raw agents", fontsize=18)

                    ax.set_title("Raw agents per language")

                plt.show()

        if event == "view":

            if not win3:

                window3 = windowtable(df.values.tolist(), df.columns.tolist())

                win3 = True

            else:

                window3.close()

                window3 = windowtable(list(df.values), list(df.columns))
