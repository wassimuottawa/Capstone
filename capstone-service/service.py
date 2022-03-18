from enum import Enum
from math import inf as infinity
from os.path import join
from shutil import move, rmtree

from flask import *
from recordclass import recordclass

from utils import *

ROOT_PATH = 'root'
ARCHIVE_FOLDER_NAME = 'archive'
ARCHIVE_PATH = join(ROOT_PATH, ARCHIVE_FOLDER_NAME)
Folder = recordclass('Folder', 'name min_detection tracklets')
Range = recordclass('Range', 'start end')


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
    image, extension = compress_image(from_root(run, folder, tracklet, file_name))
    return send_file(image, mimetype=f'image/{extension}')


def get_folders_by_run(run):
    """
    Sorting is based on the min detection time in each folder
    :returns: a sorted folder to tracklets map,
    """
    folders = []
    for folder in get_folders(from_root(run)):
        _folder = Folder(folder, str(infinity), [])
        for tracklet in get_folders(from_root(run, folder)):
            _folder.min_detection = min(get_min_detection(run, folder, tracklet),
                                        _folder.min_detection)
            _folder.tracklets.append(tracklet)
        folders.append(_folder)
    return dict(map(lambda f: (f.name, f.tracklets), sorted(folders, key=lambda f: f.min_detection)))


def get_image_names(body):
    """
    If one image in the folder is in the time range, include entire folder
    :returns: tracklet to image names map
    """
    run = body.get(Params.RUN.value)
    folder = body.get(Params.FOLDER.value)
    start = str_to_time(body.get(Params.START_TIME.value))
    end = str_to_time(body.get(Params.END_TIME.value))
    images = {}
    for tracklet in os.listdir(from_root(run, folder)):
        images[tracklet] = sort_images_by_time(get_image_names_in_path(from_root(run, folder, tracklet)))
    return images if any(is_time_range_overlaps(Range(start, end),
                                                Range(get_min_detection(run, folder, tracklet),
                                                      get_max_detection(run, folder, tracklet)))
                         for tracklet in images.keys()) \
        else {}


def get_runs():
    runs = get_folders(from_root())
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
    destination_folder = get_min_id_of_selected_folder(run, mapping)
    if destination_folder:
        mapping.pop(destination_folder, None)
    else:
        last_index = max(get_folders(from_root(run)))
        destination_folder = str(int(last_index) + 1).zfill(len(last_index))
        os.mkdir(from_root(run, destination_folder))
    move_files(run, mapping, from_root(run, destination_folder))
    return destination_folder


def get_min_id_of_selected_folder(run, files_mapping):
    """
    Determines if an entire folder is selected by the user
    If more than one entire folder is selected, determines the lowest folder id of them all
    :param files_mapping: folder to tracklets map
    :return: The lowest folder ID if entire folder is selected, else None
    """
    return next((folder for (folder, tracklets) in sorted(files_mapping.items()) if
                 len(get_folders(from_root(run, folder))) == len(tracklets)), None)


def move_files(run, files_mapping, destination):
    """
    Overwrites tracklet in destination if another one with same id is being moved
    Deletes the source folder if empty after operation
    :param files_mapping: folder to tracklets map
    :return: false if destination path already exists, or another error occurs while moving
    """
    for folder, tracklets in files_mapping.items():
        source_folder_path = from_root(run, folder)
        for tracklet in tracklets:
            new_tracklet_path = join(destination, tracklet)
            if os.path.isdir(new_tracklet_path):
                print(f'Tracklet {tracklet} exists in {destination}, overwriting..')
                rmtree(new_tracklet_path)
            move(join(source_folder_path, tracklet), destination)
        if not get_folders(source_folder_path):
            rmtree(source_folder_path)
    return True


def get_min_detection(run, folder, tracklet) -> str:
    """ Time based sorting """
    return read_file_as_dict(from_root(run, folder, tracklet, f"{tracklet}.json"))[
        TrackletData.MIN_DETECTION_TIME.value]


def get_max_detection(run, folder, tracklet) -> str:
    """ Time based sorting """
    return read_file_as_dict(from_root(run, folder, tracklet, f"{tracklet}.json"))[
        TrackletData.MAX_DETECTION_TIME.value]


def from_root(*paths):
    return join(ROOT_PATH, *paths)


if __name__ == '__main__':
    pass
