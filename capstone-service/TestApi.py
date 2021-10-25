import os

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
    lst = []
    for subdir, dirs, files in os.walk("./assets"):
        for file in files:
            if str(file).endswith(".png"):
                lst.append(os.path.basename(subdir))
                break
    return jsonify(lst)


@app.route("/folder/<string:folder>")
@cross_origin()
def getImages(folder):
    f = []
    for subdir, dirs, files in os.walk("./assets/" + folder):
        for file in files:
            if str(file).endswith(".png"):
                f.append(file)
        return jsonify(f)


if __name__ == '__main__':
    pass

# set FLASK_APP=TestApi.py
# flask run
