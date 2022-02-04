import os
from datetime import datetime
from io import BytesIO

from PIL import Image

IMAGE_EXTENSION = 'png'
TIME_FILTER_FORMAT = '%H:%M'
MAX_IMAGE_SIZE = 150, 150


def get_folders_in_path(path):
    return list(filter(lambda f: os.path.isdir(os.path.join(path, f)), os.listdir(path)))


def folder_contains_image(path):
    return any(is_image(file) for file in os.listdir(path))


def is_image(file_name):
    return str(file_name).endswith(IMAGE_EXTENSION)


def get_image_names_in_path(path):
    return list(filter(lambda f: is_image(f), os.listdir(path)))


def get_time_from_file_name(file_name):
    return datetime.fromtimestamp(float(int(os.path.splitext(file_name)[0].split(";")[5]) / pow(10, 9))).time()


def is_in_time_range(image_name, start, end):
    try:
        return True if start is None or end is None else start <= get_time_from_file_name(image_name) <= end
    except (ValueError, Exception) as e:
        print(f"{type(e)} while filtering by time for image={image_name}, start={start}, end={end}")


def str_to_time(time_string):
    if time_string is not None:
        return datetime.strptime(time_string, TIME_FILTER_FORMAT).time()


def compress_image(image_path):
    image = Image.open(image_path)
    img_io = BytesIO()
    image.thumbnail(MAX_IMAGE_SIZE)
    image.save(img_io, IMAGE_EXTENSION, quality=1, optimize=True)
    img_io.seek(0)
    return img_io, IMAGE_EXTENSION
