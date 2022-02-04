import os
from datetime import datetime

IMAGE_EXTENSION = '.png'
TIME_FILTER_FORMAT = '%H:%M'


def folder_contains_image(path):
    for file in os.listdir(path):
        if is_image(file):
            return True
    return False


def is_image(file_name):
    return str(file_name).endswith(IMAGE_EXTENSION)


def get_image_names_in_path(path):
    return list(filter(lambda f: is_image(f), os.listdir(path)))


def get_time_from_file_name(file_name):
    return datetime.fromtimestamp(float(int(os.path.splitext(file_name)[0].split(";")[5]) / pow(10, 9))).time()


def is_in_time_range(image_name, start, end):
    try:
        if start is None or end is None:
            return True
        time = get_time_from_file_name(image_name)
        return start <= time <= end
    except ValueError:
        print("ValueError caught while filtering by time for image={0}, start={1}, end={2}".format(image_name, start,
                                                                                                   end))
        return False


def str_to_time(time_string):
    if time_string is not None:
        return datetime.strptime(time_string, TIME_FILTER_FORMAT).time()
