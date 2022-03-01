import json
import os
from datetime import datetime
from io import BytesIO

from PIL import Image

SOURCE_IMAGE_EXTENSION = 'png'
COMPRESSED_IMAGE_FORMAT = 'webp'
TIME_FILTER_FORMAT = '%H:%M'
MAX_IMAGE_SIZE = 150, 150
MAX_UNIX_DATE = datetime(2999, 12, 31, 23, 59, 59, 999999).timestamp()


def get_folders(path):
    return list(filter(lambda f: os.path.isdir(os.path.join(path, f)), os.listdir(path)))


def is_image(file_name):
    return str(file_name).endswith(SOURCE_IMAGE_EXTENSION)


def get_image_names(path):
    return list(filter(lambda f: is_image(f), os.listdir(path)))


def get_time_from_file_name(file_name):
    return datetime.fromtimestamp(get_unix_date_from_file_name(file_name)).time()


def get_unix_date_from_file_name(file_name):
    try:
        return float(int(os.path.splitext(file_name)[0].split(";")[5])) / 1e9
    except (ValueError, Exception) as e:
        print(f"{get_error_name(e)}: image={file_name} does not match the predefined filename format")
        return MAX_UNIX_DATE


def is_in_time_range(image_name, start, end):
    try:
        return True if start is None or end is None else start <= get_time_from_file_name(image_name) <= end
    except (ValueError, Exception) as e:
        print(f"{get_error_name(e)}: unable to filter by time for image={image_name}, start={start}, end={end}")


def str_to_time(time_string):
    if time_string is not None:
        return datetime.strptime(time_string, TIME_FILTER_FORMAT).time()


def compress_image(image_path):
    image = Image.open(image_path)
    img_io = BytesIO()
    image.thumbnail(MAX_IMAGE_SIZE)
    image.save(img_io, format=COMPRESSED_IMAGE_FORMAT, quality=15, optimize=True)
    img_io.seek(0)
    return img_io, COMPRESSED_IMAGE_FORMAT


def sort_images_by_time(image_names: list):
    return sorted(image_names, key=lambda img: get_unix_date_from_file_name(img))


def read_file_as_dict(path):
    with open(path, 'r') as f:
        return json.load(f)


def get_error_name(e: Exception):
    return type(e).__name__


if __name__ == '__main__':
    pass
