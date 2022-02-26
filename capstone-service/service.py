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


# Sorts by scanning directory to find lowest detection time.
def get_folders_by_run(run):
    """ :returns: a sorted folder to tracklets map"""
    folders = []
    folder_data = dict()
    for folder in get_folders_in_path(os.path.join(ROOT_PATH, run)):
        tracklet_data = dict()

        for tracklet in get_folders_in_path(os.path.join(ROOT_PATH, run, folder)):
            images = get_image_names_in_path(os.path.join(ROOT_PATH, run, folder, tracklet))
            sorted_images = sort_images_by_time(images)
            min_detection_time = get_time_from_file_name(sorted_images[0])
            tracklet_data[tracklet] = min_detection_time

        folders.append({ folder: list(tracklet_data.keys()) })
        folder_data[folder] = min(tracklet_data.values())

    folders = sorted(folders, key=lambda x: folder_data[list(x.keys())[0]])
    return folders


# Sorts by getting lowest detection time from JSON file.
def get_folders_by_run_v2(run):
    """ :returns: a sorted folder to tracklets map"""
    folders = []
    folder_data = dict()
    for folder in get_folders_in_path(os.path.join(ROOT_PATH, run)):
        tracklet_data = dict()

        for tracklet in get_folders_in_path(os.path.join(ROOT_PATH, run, folder)):
            path = os.path.join(ROOT_PATH, run, folder, tracklet, f"{tracklet}.json")
            contents = read_json_file_into_dict(path)
            min_detection_time = float(int(contents["min_detection_time"]) / pow(10, 9))
            tracklet_data[tracklet] = min_detection_time
        
        folders.append({ folder: list(tracklet_data.keys()) })
        folder_data[folder] = min(tracklet_data.values())

    folders = sorted(folders, key=lambda x: folder_data[list(x.keys())[0]])
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
    :return: true and lowestFolderId if entire folder is selected, else false
    """
    return next((folder for (folder, tracklets) in sorted(files_mapping.items()) if len(get_folders_in_path(os.path.join(ROOT_PATH, run, folder))) == len(tracklets)), None)

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
