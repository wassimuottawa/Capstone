import datetime
import io
import time

import matplotlib.pyplot as plt
import numpy as np
from flask import send_file

import stats_generator_service as gen

IMAGE_FORMAT = 'png'


def service_time_graph():
    plt.figure(figsize=(20, 8))
    plt.title("Service time ranges", pad=20)

    x = np.array(["Average service time", "Minimum service time", "Maximum service time"])
    yLabel = np.array([gen.generated_stats.average_service_time, gen.generated_stats.min_service_time,
                       gen.generated_stats.max_service_time])
    y = np.array(list(map(lambda t: to_seconds(t), yLabel)))
    plt.barh(x, y, color=['black', 'blue', 'blue'])
    plt.xlabel("Time", labelpad=20)
    plt.xticks(y, yLabel)
    plt.gcf().subplots_adjust(left=0.20)
    return send_file(to_image(plt), mimetype=f'image/{IMAGE_FORMAT}')


def service_time_distribution_graph():
    plt.figure(figsize=(20, 8))
    plt.title("Total average service time distribution", pad=20)

    val = np.array([gen.generated_stats.less_1, gen.generated_stats.bet_1_3, gen.generated_stats.bet_3_5,
                    gen.generated_stats.bet_5_10, gen.generated_stats.bet_10_15, gen.generated_stats.more_15])
    label = ["Less than 1 minute", "Between 1 and 3 minutes", "Between 3 and 5 minutes", "Between 5 and 10 minutes",
             "Between 10 and 15 minutes", "More than 15 minutes"]
    plt.pie(val, labels=label)
    return send_file(to_image(plt), mimetype=f'image/{IMAGE_FORMAT}')


def distribution_by_time_interval_graph():
    plt.figure(figsize=(20, 8))
    plt.title("Distribution by time", pad=20)

    t = list(map(lambda x: format_nano(x), gen.generated_stats.breakdown_stats.keys()))
    breakdown_stats = list(gen.generated_stats.breakdown_stats.values())

    customers = list(map(lambda h: h['num_customers'], breakdown_stats))
    max_customers = max(customers)
    customers_formatted = list(map(lambda x: x / max_customers, customers))

    avgs = list(map(lambda h: h.get('average_time', "00:00"), breakdown_stats))
    avgs_seconds = list(map(lambda h: to_seconds(h.get('average_time', "00:00")), breakdown_stats))
    max_avg = max(avgs_seconds)
    avg_formatted = list(map(lambda x: x / max_avg, avgs_seconds))

    for i in range(0, len(t)):
        plt.annotate(customers[i], (t[i], customers_formatted[i]), textcoords="offset points", xytext=(0, 10),
                     color='blue', ha='center')
        plt.annotate(avgs[i], (t[i], avg_formatted[i]), textcoords="offset points", color='orange', ha='center',
                     xytext=(0, 10 if abs(customers_formatted[i] - avg_formatted[i]) > 0.2 else -10))

    plt.plot(t, customers_formatted, label="Number of customers")
    plt.plot(t, avg_formatted, label="Average service time")
    plt.xlabel("Time", labelpad=20)
    plt.yticks([])
    plt.autoscale()
    plt.legend()
    return send_file(to_image(plt), mimetype=f'image/{IMAGE_FORMAT}')


def to_seconds(time_str):
    x = time.strptime(time_str.split(',')[0], '%M:%S')
    return datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()


def format_nano(nanos):
    dt = datetime.datetime.fromtimestamp(nanos / 1e9)
    return '{}'.format(dt.strftime('%H:%M'), nanos % 1e2)


def to_image(plot):
    img_io = io.BytesIO()
    plot.savefig(img_io, format=IMAGE_FORMAT)
    img_io.seek(0)
    return img_io


if __name__ == '__main__':
    pass
