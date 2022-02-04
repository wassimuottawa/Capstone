from flask import *
from flask_cors import cross_origin, CORS

import service

app = Flask(__name__)
cors = CORS(app)


@app.route("/image/<string:run>/<string:folder>/<string:tracklet>/<string:image>")
@cross_origin()
def get_image(run, folder, tracklet, image):
    return service.get_compressed_image_file(run, folder, tracklet, image)


@app.route("/delete", methods=['POST'])
@cross_origin()
def delete_tracklets():
    return Response(status=200) if service.delete_tracklets(request.json) else Response(status=400)


@app.route("/runs")
@cross_origin()
def get_runs():
    return jsonify(service.get_runs())


@app.route("/folder/<string:run>")
@cross_origin()
def get_folders_by_run(run):
    """ :returns: a folder to tracklets map"""
    return jsonify(service.get_folders_by_run(run))


@app.route("/trackletsToImages", methods=['POST'])
@cross_origin()
def get_tracklets_to_image_names_map():
    """ :returns: tracklet to image names map """
    return jsonify(service.get_image_names(request.json))


@app.route("/extract", methods=['POST'])
@cross_origin()
def extract():
    """ :returns: the new folder name """
    return jsonify(service.extract_into_new_folder(request.json))


if __name__ == '__main__':
    pass

# set FLASK_APP=api.py
# flask run
