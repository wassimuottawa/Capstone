import os
import datetime

from flask import *
from flask_cors import cross_origin

app = Flask(__name__)


@app.route("/image/<string:folder>/<string:image>")
@cross_origin()
def getFile(folder, image):
    return send_from_directory("./assets/" + folder, image)


@app.route("/folders")
@cross_origin()
def getFolders():
    dirs, files = get_dir_content("./assets")
    return jsonify(dirs)


@app.route("/folder/<string:folder>")
@cross_origin()
def getImages(folder):
    dirs, files = get_dir_content("./assets/" + folder, ".png")
    return jsonify(files)
    

# Gets all immediate subdirectories and all immediate files (or only files with a ceratin extension) in a directory
def get_dir_content(path, extensions = ''):
    subdirs_list = []
    files_list = []
    for root, dirs, files in os.walk(path):
        subdirs_list = dirs
        
        if extensions:
            for f in files:
                if f.endswith(extensions):
                    files_list.append(f)
        else:
            files_list += files
        
        break
    return (subdirs_list, files_list)

# Returns all images in a specific date range
def get_images_in_date_range(path, start_y, start_m, stary_d, end_y, end_m, end_d):
    start_date = datetime(start_y, start_m, stary_d)
    end_date   = datetime(end_y, end_m, end_d)
    files_in_range = []

    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.png'):
                file_name = os.path.splitext(f)[0] # Remove file extension
                img_date = datetime.fromtimestamp(float(file_name) / 1e9) # Divide to convert to secs
                
                if ((img_date >= start_date) and (img_date <= end_date)):
                    files_in_range.append(os.path.join(root, f))
    
    return files_in_range


if __name__ == '__main__':
    pass

# set FLASK_APP=TestApi.py
# flask run
