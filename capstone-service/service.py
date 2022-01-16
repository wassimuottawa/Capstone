import os
import shutil
from datetime import datetime
from enum import Enum

from flask import *

ROOT_PATH = 'root'
IMAGE_EXTENSION = '.png'
ARCHIVE_FOLDER = 'archive'
ARCHIVE_PATH = os.path.join(ROOT_PATH, ARCHIVE_FOLDER)
TIME_FILTER_FORMAT = '%H:%M'


# JSON keys from UI
class Params(Enum):
    RUN = 'run'
    FOLDER = 'folder'
    START_TIME = 'start'
    END_TIME = 'end'
    DESTINATION_FOLDER = 'destinationFolder'
    MAPPING = 'mapping'


def get_folders_in_path(path):
    return list(filter(lambda f: os.path.isdir(os.path.join(path, f)), os.listdir(path)))


def get_folders_by_run(run):
    folders = set()
    for folder in get_folders_in_path(os.path.join(ROOT_PATH, run)):
        if folder_contains_image(run, folder):
            folders.add(folder)
    return folders


def file_exists(run, folder, file):
    return os.path.isfile(os.path.join(ROOT_PATH, run, folder, file))


def folder_exists(run, folder):
    return os.path.isdir(os.path.join(ROOT_PATH, run, folder))


def get_image_file(run, folder, file_name):
    return send_from_directory(os.path.join(ROOT_PATH, run, folder), file_name)


def folder_contains_image(run, folder):
    for file in os.listdir(os.path.join(ROOT_PATH, run, folder)):
        if is_image(file):
            return True
    return False


# If one image in the folder is in the time range, include entire folder
def get_image_names(body):
    run = body.get(Params.RUN.value)
    folder = body.get(Params.FOLDER.value)
    start = str_to_time(body.get(Params.START_TIME.value))
    end = str_to_time(body.get(Params.END_TIME.value))
    images = set()
    for img in get_image_names_in_path(run, folder):
        images.add(img)
    return images if any(is_in_time_range(img, start, end) for img in images) else {}


def is_image(file_name):
    return str(file_name).endswith(IMAGE_EXTENSION)


def get_image_names_in_path(run, folder):
    return list(filter(lambda f: is_image(f), os.listdir(os.path.join(ROOT_PATH, run, folder))))


def get_runs():
    runs = get_folders_in_path(ROOT_PATH)
    runs.remove(ARCHIVE_FOLDER)
    return runs


def delete_files(body: dict):
    move_files(body.get(Params.RUN.value), body.get(Params.MAPPING.value), ARCHIVE_PATH)


def move(body: dict):
    run = body.get(Params.RUN.value)
    destination_path = os.path.join(ROOT_PATH, run, body.get(Params.DESTINATION_FOLDER.value))
    move_files(run, body.get(Params.MAPPING.value), destination_path)


def move_files(run, files_mapping, destination, overwrite=True):
    for folder, files in files_mapping.items():
        for file in files:
            if file_exists(run, folder, file):
                shutil.move(os.path.join(ROOT_PATH, run, folder, file),
                            os.path.join(destination, file) if overwrite else destination)
                break


def get_time_from_file_name(file_name):
    return datetime.fromtimestamp(float(os.path.splitext(file_name)[0])).time()


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


if __name__ == '__main__':
    pass
