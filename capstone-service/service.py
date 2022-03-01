import math
import shutil
from enum import Enum

from flask import *
from recordclass import recordclass

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


# JSON keys for tracklet data file
class TrackletData(Enum):
    MIN_DETECTION_TIME = 'min_detection_time'
    MAX_DETECTION_TIME = 'max_detection_time'
    NUMBER_OF_DETECTIONS = 'num_detections'


def get_compressed_image_file(run, folder, tracklet, file_name):
    image, extension = compress_image(os.path.join(ROOT_PATH, run, folder, tracklet, file_name))
    return send_file(image, mimetype=f'image/{extension}')


def get_folders_by_run(run):
    """
    sorting is based on the min detection time in each folder
    :returns: a sorted folder to tracklets map,
    """
    Folder = recordclass('Folder', 'name min_detection tracklets')
    folders = []
    for folder in get_folders_in_path(os.path.join(ROOT_PATH, run)):
        _folder = Folder(folder, str(math.inf), [])
        for tracklet in get_folders_in_path(os.path.join(ROOT_PATH, run, folder)):
            _folder.min_detection = min(get_min_detection_time_by_tracklet(run, folder, tracklet),
                                        _folder.min_detection)
            _folder.tracklets.append(tracklet)
        folders.append(_folder)
    return dict(map(lambda f: (f.name, f.tracklets), sorted(folders, key=lambda f: f.min_detection)))


def get_min_detection_time_by_tracklet(run, folder, tracklet):
    return read_file_as_dict(os.path.join(ROOT_PATH, run, folder, tracklet, f"{tracklet}.json"))[
        TrackletData.MIN_DETECTION_TIME.value]


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
    os.makedirs(ARCHIVE_PATH, exist_ok=True)
    return move_files(body.get(Params.RUN.value), body.get(Params.MAPPING.value), ARCHIVE_PATH)


def extract_into_new_folder(body: dict):
    """
    If an entire folder is selected by the user, the remaining selected tracklets
    are added to the folder with the lowest Id
    If no full folder is selected, a new folder is created for the selected tracklets
    :param body: folder to tracklets map
    """
    run = body.get(Params.RUN.value)
    mapping: dict = body.get(Params.MAPPING.value)
    destination_folder = get_lowest_id_of_selected_folder(run, mapping)
    if destination_folder:
        mapping.pop(destination_folder, None)
    else:
        last_index = max(get_folders_in_path(os.path.join(ROOT_PATH, run)))
        destination_folder = str(int(last_index) + 1).zfill(len(last_index))
        os.mkdir(os.path.join(ROOT_PATH, run, destination_folder))
    move_files(run, mapping, os.path.join(ROOT_PATH, run, destination_folder))

    return destination_folder


def get_lowest_id_of_selected_folder(run, files_mapping):
    """
    Determines if an entire folder is selected by the user
    If more than one entire folder is selected, determines the lowest folder id of them all
    :param files_mapping: folder to tracklets map
    :return: The lowest folder ID if entire folder is selected, else None
    """
    return next((folder for (folder, tracklets) in sorted(files_mapping.items()) if
                 len(get_folders_in_path(os.path.join(ROOT_PATH, run, folder))) == len(tracklets)), None)


def move_files(run, files_mapping, destination):
    """
    Overwrites tracklet in destination if another one with same id is being moved
    Deletes the source folder if empty after move
    :param files_mapping: folder to tracklets map
    :return: false if destination path already exists, or another error occurs while moving
    """
    for folder, tracklets in files_mapping.items():
        source_folder_path = os.path.join(ROOT_PATH, run, folder)
        for tracklet in tracklets:
            new_tracklet_path = os.path.join(destination, tracklet)
            if os.path.isdir(new_tracklet_path):
                print(f'Tracklet {tracklet} exists in {destination}, overwriting..')
                shutil.rmtree(new_tracklet_path)
            shutil.move(os.path.join(source_folder_path, tracklet), destination)
        if not get_folders_in_path(source_folder_path):
            shutil.rmtree(source_folder_path)
    return True


if __name__ == '__main__':
    pass
