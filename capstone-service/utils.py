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


def get_image_names_in_path(path):
    return list(filter(lambda f: is_image(f), os.listdir(path)))


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


# Strip the date part from the timestamp
def get_time_from_timestamp(timestamp: str) -> datetime.time:
    return datetime.fromtimestamp(float(timestamp) / 1e9).time().replace(microsecond=0)


def get_unix_date_from_file_name(file_name) -> str:
    try:
        return os.path.splitext(file_name)[0].split(";")[5]
    except (ValueError, Exception) as e:
        print(f"{get_error_name(e)}: image={file_name} does not match the predefined filename format")
        return str(MAX_UNIX_DATE)


def is_time_range_overlaps(optional_ui_range, range2) -> bool:
    try:        return True if optional_ui_range.start is None or optional_ui_range.end is None else optional_ui_range.start <= get_time_from_timestamp(
            range2.end) and get_time_from_timestamp(range2.start) < optional_ui_range.end
    except (ValueError, Exception) as e:
        print(
            f"{get_error_name(e)}: unable to filter by time for range [{range2.start},{range2.end}], given start={optional_ui_range.start}, end={optional_ui_range.end}")


def str_to_time(time_string: str) -> datetime.time:
    if time_string is not None:
        return datetime.strptime(time_string, TIME_FILTER_FORMAT).time()


def get_error_name(e: Exception):
    return type(e).__name__


if __name__ == '__main__':
    pass
