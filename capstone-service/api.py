from flask import *
from flask_cors import cross_origin, CORS

import service

app = Flask(__name__)
cors = CORS(app)


@app.route("/image/<string:run>/<string:folder>/<string:tracklet>/<string:image>")
@cross_origin()
def get_image(run, folder, tracklet, image):
    return service.get_image_file(run, folder, tracklet, image)


@app.route("/delete", methods=['POST'])
@cross_origin()
def delete_images():
    success = service.delete_files(request.json)
    if success:
        return Response(status=200)
    else:
        return Response(status=400)


@app.route("/runs")
@cross_origin()
def get_runs():
    return jsonify(service.get_runs())


@app.route("/folder/<string:run>")
@cross_origin()
def get_folders_by_run(run):
    return jsonify(service.get_folders_by_run(run))


@app.route("/images", methods=['POST'])
@cross_origin()
def get_image_names():
    return jsonify(service.get_image_names(request.json))


@app.route("/move", methods=['POST'])
@cross_origin()
def move():
    success = service.move(request.json)
    if success:
        return Response(status=200)
    else:
        return Response(status=400)


if __name__ == '__main__':
    pass

# set FLASK_APP=api.py
# flask run
