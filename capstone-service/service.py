import os
import shutil
from datetime import datetime

from flask import *

ROOT_PATH = 'root'
IMAGE_EXTENSION = '.png'
ARCHIVE_FOLDER = 'archive'
ARCHIVE_PATH = os.path.join(ROOT_PATH, ARCHIVE_FOLDER)

# JSON keys from UI
RUN_PARAM = 'run'
FOLDER_PARAM = 'folder'
START_TIME_PARAM = 'start'
END_TIME_PARAM = 'end'
DESTINATION_PARAM = 'destination'
MAPPING_PARAM = 'mapping'


def get_folders_in_path(path):
    return list(filter(lambda f: os.path.isdir(os.path.join(path, f)), os.listdir(path)))


def get_folders_by_run(run):
    folders = set()
    for cam in get_cams(run):
        for folder in get_folders_in_path(os.path.join(ROOT_PATH, run, cam)):
            if not_empty(run, cam, folder):
                folders.add(folder)
    return folders


def get_cams(run):
    return get_folders_in_path(os.path.join(ROOT_PATH, run))


def file_exists(run, cam, folder, file):
    return os.path.isfile(os.path.join(ROOT_PATH, run, cam, folder, file))


def folder_exists(run, cam, folder):
    return os.path.isdir(os.path.join(ROOT_PATH, run, cam, folder))


def get_file(run, folder, file):
    for cam in get_cams(run):
        if file_exists(run, cam, folder, file):
            return send_from_directory(os.path.join(ROOT_PATH, run, cam, folder), file)


def not_empty(run, cam, folder):
    for file in os.listdir(os.path.join(ROOT_PATH, run, cam, folder)):
        if is_image(file):
            return True
    return False


def get_image_names(body):
    run = body.get(RUN_PARAM)
    folder = body.get(FOLDER_PARAM)
    start = str_to_time(body.get(START_TIME_PARAM))
    end = str_to_time(body.get(END_TIME_PARAM))
    images = set()
    for cam in list(filter(lambda c: folder_exists(run, c, folder), get_cams(run))):
        for img in os.listdir(os.path.join(ROOT_PATH, run, cam, folder)):
            if is_image(img) and is_in_time_range(img, start, end):
                images.add(img)
    return images


def is_image(file_name):
    return str(file_name).endswith(IMAGE_EXTENSION)


def get_runs():
    runs = get_folders_in_path(ROOT_PATH)
    runs.remove(ARCHIVE_FOLDER)
    return runs


def delete_files(body: dict):
    move_files(body.get(RUN_PARAM), body.get(MAPPING_PARAM), ARCHIVE_PATH)


def move(body: dict):
    run = body.get(RUN_PARAM)
    destination = os.path.join(ROOT_PATH, run, get_cams(run)[0], body.get(DESTINATION_PARAM))
    move_files(run, body.get(MAPPING_PARAM), destination)


def move_files(run, files_mapping, destination):
    for folder, files in files_mapping.items():
        for file in files:
            for cam in get_cams(run):
                if file_exists(run, cam, folder, file):
                    shutil.move(os.path.join(ROOT_PATH, run, cam, folder, file), destination)
                    break


def get_time_from_file_name(file_name):
    return datetime.fromtimestamp(float(os.path.splitext(file_name)[0])).time()


def is_in_time_range(image_name, start, end):
    if start is None or end is None:
        return True
    time = get_time_from_file_name(image_name)
    return start <= time <= end


def str_to_time(time_string):
    if time_string is not None:
        return datetime.strptime(time_string, '%H:%M').time()


if __name__ == '__main__':
    pass
