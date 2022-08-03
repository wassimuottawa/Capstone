from collections import OrderedDict
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from recordclass import recordclass

import utils

Stats = recordclass('Stats',
                    'data_date num_customers less_1 bet_1_3 bet_3_5 bet_5_10 bet_10_15 more_15 min_service_time max_service_time average_service_time breakdown_stats')
generated_stats = None
data_dict = {}
Range = recordclass('Range', 'name start end')
breakfast = Range('Breakfast', '06:00', '10:00')
lunch = Range('Lunch', '10:30', '13:30')
snack = Range('Snack', '14:00', '16:30')
dinner = Range('Dinner', '17:00', '19:30')
late_night = Range('Late Night', '20:00', '21:30')
ranges = [breakfast, lunch, snack, dinner, late_night]


def str_to_ns(time_str):
    """
    input: time in a format `hh:mm:ss.up_to_9_digits`
    """
    h, m, s = time_str.split(":")
    int_s, ns = s.split(".")
    ns = map(lambda t, unit: np.timedelta64(t, unit),
             [h, m, int_s, ns.ljust(9, '0')], ['h', 'm', 's', 'ns'])
    return int(sum(ns))


def nano_to_readable(nano):
    nanos = int(nano)
    seconds = (nanos / 1000000000) % 60
    seconds = int(seconds)
    minutes = (nanos / (1000000000 * 60)) % 60
    minutes = int(minutes)

    minutes_str = str(minutes)
    if len(minutes_str) < 2:
        minutes_str = "0" + minutes_str

    seconds_str = str(seconds)
    if len(seconds_str) < 2:
        seconds_str = "0" + seconds_str

    return minutes_str + ":" + seconds_str


def get_num_customers(data):
    return len(data["customers"])


def get_elapsed_list(data):
    elapsed_list = []
    for customer_id in data["customers"]:
        f_app = int(data["customers"][customer_id]["first_appear"])
        l_app = int(data["customers"][customer_id]["last_appear"])
        el = l_app - f_app
        # secs = el / 1e9
        # dt = datetime.fromtimestamp(secs)
        # v = dt.strftime('%M:%S.%f')

        # elapsed = (l_app - f_app)/60000000000
        elapsed_list.append(el)

    return elapsed_list  # min_service_time, max_service_time, average_service_time


def get_elapsed_stats(elapsed_list):
    less_1 = 0
    bet_1_3 = 0
    bet_3_5 = 0
    bet_5_10 = 0
    bet_10_15 = 0
    more_15 = 0

    one_minute = 6e+10
    three_minutes = 1.8e+11
    five_minutes = 3e+11
    ten_minutes = 6e+11
    fifteen_minutes = 9e+11

    for elapsed in elapsed_list:
        if elapsed <= one_minute:
            less_1 += 1
        elif one_minute < elapsed <= three_minutes:
            bet_1_3 += 1
        elif three_minutes < elapsed <= five_minutes:
            bet_3_5 += 1
        elif five_minutes < elapsed <= ten_minutes:
            bet_5_10 += 1
        elif ten_minutes < elapsed <= fifteen_minutes:
            bet_10_15 += 1
        elif elapsed > fifteen_minutes:
            more_15 += 1
    total_processed = less_1 + bet_1_3 + bet_3_5 + bet_5_10 + bet_10_15 + more_15
    return less_1, bet_1_3, bet_3_5, bet_5_10, bet_10_15, more_15


def breakdown(data, data_date, start_time, end_time, interval_min=45):
    intervals_list = []  # to store interval values
    intervals_dict = OrderedDict()  # to contain interval statistics

    start_dt = data_date.replace(hour=start_time[0], minute=start_time[1], second=0,
                                 microsecond=0)  # setting data start datetime object
    end_dt = data_date.replace(hour=end_time[0], minute=end_time[1], second=0,
                               microsecond=0)  # setting data end datetime object

    start_t = int(start_dt.timestamp() * 1000000000)  # setting data start datetime timestamp
    end_t = int(end_dt.timestamp() * 1000000000)  # setting data end datetime timestamp

    curr_timestamp = start_t

    while curr_timestamp <= end_t:  # creating the intervals
        intervals_list.append(curr_timestamp)
        intervals_dict[curr_timestamp] = OrderedDict()
        intervals_dict[curr_timestamp]["num_customers"] = 0
        intervals_dict[curr_timestamp]["sum_elapsed"] = 0

        curr_timestamp += int(interval_min * (6e+10))

    for customer_id in data["customers"]:  # looping through customers, adding customer stats in appropriate interval
        customer_first_appear = int(data["customers"][customer_id]["first_appear"])
        for i in range(len(intervals_list)):
            if customer_first_appear <= intervals_list[i]:
                intervals_dict[intervals_list[i]][
                    "num_customers"] += 1  # keeping track of number of customers during this time range
                f_app = int(data["customers"][customer_id]["first_appear"])
                customer_last_appear = int(data["customers"][customer_id]["last_appear"])
                intervals_dict[intervals_list[i]]["sum_elapsed"] += customer_last_appear - customer_first_appear
                break

    for interval in intervals_list:
        if intervals_dict[interval]["num_customers"] != 0:
            intervals_dict[interval]["average_time"] = nano_to_readable(
                int(intervals_dict[interval]["sum_elapsed"] / intervals_dict[interval]["num_customers"]))
    return intervals_dict


def get_data_date(data):
    for customer in data["customers"]:
        timestamp = int(data["customers"][customer]["first_appear"])
        dt = datetime.fromtimestamp(timestamp // 1000000000)
        return dt


def load_data(data):
    global data_dict
    data_dict = data


def generate_stats(data):
    load_data(data)
    data_date = get_data_date(data_dict)

    num_customers = get_num_customers(data_dict)
    elapsed_list = get_elapsed_list(data_dict)
    less_1, bet_1_3, bet_3_5, bet_5_10, bet_10_15, more_15 = get_elapsed_stats(elapsed_list)

    min_service_time = nano_to_readable(min(elapsed_list))
    max_service_time = nano_to_readable(max(elapsed_list))
    average_service_time = nano_to_readable(np.mean(elapsed_list))

    breakdown_stats = breakdown(data_dict, data_date, (12, 30, 0, 0),
                                (14, 0, 0, 0))  # str_to_ns("12:30:00."), str_to_ns("14:00:00."))
    global generated_stats
    generated_stats = Stats(data_date, num_customers, less_1, bet_1_3, bet_3_5, bet_5_10, bet_10_15, more_15,
                            min_service_time, max_service_time, average_service_time, breakdown_stats)
    print("Stats generated")


def get_tickets_by_interval():
    df = pd.DataFrame(
        {
            "first_appear": list(
                map(lambda x: utils.get_time_from_timestamp(x['first_appear']), data_dict['customers'].values())),
            "last_appear": list(
                map(lambda x: utils.get_time_from_timestamp(x['last_appear']), data_dict['customers'].values()))
        }
    )
    interval = 30
    IntFrame = pd.DataFrame(
        {"interval": [(datetime.min + i * timedelta(minutes=interval)).time() for i in
                      range(6 * 60 // interval, int(22.5 * 60) // interval)],
         "tickets": 0}
    )
    for index1, index2 in zip(IntFrame.index.values[:-1], IntFrame.index.values[1:]):
        for i in df.index.values:
            first = df.loc[i, "first_appear"]
            last = df.loc[i, "last_appear"]
            if IntFrame.loc[index1, "interval"] <= first < IntFrame.loc[index2, "interval"]:
                IntFrame.loc[index1, "tickets"] += 1
                if last >= IntFrame.loc[index2, "interval"]:
                    Index3 = max(IntFrame.where(last >= IntFrame["interval"]).dropna().index.values)
                    IntFrame.loc[index2:Index3, "tickets"] += 1
    return construct_ranges(
        [(str(k)[:-3], v) for (k, v) in IntFrame.set_index('interval').to_dict()['tickets'].items()])


def subtract_minute(str):
    h, m = str.split(":")
    return h + ":29" if m == '30' else h + ':59'


def construct_ranges(lst):
    result = dict()
    for i in range(len(lst) - 1):
        for rng in ranges:
            if rng.name not in result:
                result[rng.name] = []
            if rng.start <= lst[i][0] < rng.end:
                result[rng.name].append({
                    'from': lst[i][0],
                    'to': subtract_minute(lst[i + 1][0]),
                    'tickets': lst[i][1],
                })
                break
    return result
