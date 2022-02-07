import shutil
from enum import Enum

from flask import *

from utils import *

ROOT_PATH = 'root'
ARCHIVE_FOLDER_NAME = 'archive'
ARCHIVE_PATH = os.path.join(ROOT_PATH, ARCHIVE_FOLDER_NAME)


# JSON keys from UI
class Params(Enum):
    RUN = 'run'
    FOLDER = 'folder'
    START_TIME = 'start'
    END_TIME = 'end'
    MAPPING = 'mapping'


def get_compressed_image_file(run, folder, tracklet, file_name):
    image, extension = compress_image(os.path.join(ROOT_PATH, run, folder, tracklet, file_name))
    return send_file(image, mimetype=f'image/{extension}')


def get_folders_by_run(run):
    """ :returns: a folder to tracklets map"""
    folders = dict()
    for folder in get_folders_in_path(os.path.join(ROOT_PATH, run)):
        folders[folder] = []
        for tracklet in get_folders_in_path(os.path.join(ROOT_PATH, run, folder)):
            if folder_contains_image(os.path.join(ROOT_PATH, run, folder, tracklet)):
                folders[folder].append(tracklet)
    return folders


def get_image_names(body):
    """ If one image in the folder is in the time range, include entire folder
        :returns: tracklet to image names map
    """
    run = body.get(Params.RUN.value)
    folder = body.get(Params.FOLDER.value)
    start = str_to_time(body.get(Params.START_TIME.value))
    end = str_to_time(body.get(Params.END_TIME.value))
    images = {}
    for tracklet in os.listdir(os.path.join(ROOT_PATH, run, folder)):
        images[tracklet] = sort_images_by_time(get_image_names_in_path(os.path.join(ROOT_PATH, run, folder, tracklet)))
    return images if any(is_in_time_range(img, start, end) for tracklet in images.values() for img in tracklet) else {}


def get_runs():
    runs = get_folders_in_path(ROOT_PATH)
    runs.remove(ARCHIVE_FOLDER_NAME)
    return runs


def delete_tracklets(body: dict):
    """ :param body: folder to tracklets map """
    return move_files(body.get(Params.RUN.value), body.get(Params.MAPPING.value), ARCHIVE_PATH)


def extract_into_new_folder(body: dict):
    """ :param body: folder to tracklets map """
    run = body.get(Params.RUN.value)
    last_index = get_folders_in_path(os.path.join(ROOT_PATH, run))[-1]
    new_folder_name = str(int(last_index) + 1).zfill(len(last_index))
    new_folder_path = os.path.join(ROOT_PATH, run, new_folder_name)
    os.mkdir(new_folder_path)
    move_files(run, body.get(Params.MAPPING.value), new_folder_path)
    return new_folder_name


def move_files(run, files_mapping, destination):
    """
    :param files_mapping: folder to tracklets map
    :return: false if destination path already exists, or another error occurs while moving
    """
    for folder, tracklets in files_mapping.items():
        source_folder_path = os.path.join(ROOT_PATH, run, folder)
        for tracklet in tracklets:
            shutil.move(os.path.join(source_folder_path, tracklet), destination)
        if not get_folders_in_path(source_folder_path):
            os.remove(source_folder_path)
    return True


if __name__ == '__main__':
    pass
