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
    os.makedirs(ARCHIVE_PATH, exist_ok=True)
    return move_files(body.get(Params.RUN.value), body.get(Params.MAPPING.value), ARCHIVE_PATH)


def extract_into_new_folder(body: dict):
    """ :param body: folder to tracklets map """
    run = body.get(Params.RUN.value)
    last_index = max(get_folders_in_path(os.path.join(ROOT_PATH, run)))
    new_folder_name = str(int(last_index) + 1).zfill(len(last_index))
    new_folder_path = os.path.join(ROOT_PATH, run, new_folder_name)

    print(entireFolderSelected(run, body.get(Params.MAPPING.value))) # Checks if entire folder is selected and prints the lowest id of all selected folders

    os.mkdir(new_folder_path)
    move_files(run, body.get(Params.MAPPING.value), new_folder_path)
    return new_folder_name

def entireFolderSelected(run, files_mapping):
    """
    Determines if an entire folder is selected by the user
    If more than one entire folder is selected, determines the lowest folder id of them all
    :param files_mapping: folder to tracklets map
    :return: true and lowestFolderId if entire folder is selected, else false
    """
    dictionary = get_folders_by_run(run)                                                    # full dictionary of all folders and their respective tracklets
    lowestFolderId = 99999                                                                   # dummy value for lowestFolderId
    for folder, tracklets in files_mapping.items():                                         # iterates through all folders and tracklets of the mapped/ user selected folders and tracklets
        selectedTracklets = set(tracklets)                                                  # creates a set for the selected tracklets from within a folder
        for key, value in dictionary.items():                                               # iterates through all key(folder) and values (tracklets) in the dictionary of all folders and tracklets
                if key == folder:                                                           # Hits when a user selected folder is found in dictionary of all folders
                    allFolderTracklets = set(value)                                         # creates set of all tracklets within dictionary folder
                if selectedTracklets == set(value) and (int(folder) < int(lowestFolderId)): # if all tracklets in user selected folder are all the tracklets within folder, and, the id of folder is the lowest of all selected folders, hits
                    lowestFolderId = folder                                                 # sets value for lowest folder
                    return True,lowestFolderId                                              # returns true the lowestFolderId for the tracklets to be merged into
    return False                                                                            # else false

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
