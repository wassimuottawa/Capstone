from flask import *
from flask_cors import cross_origin, CORS

import service

app = Flask(__name__)
cors = CORS(app)


@app.route("/image/<string:run>/<string:folder>/<string:image>")
@cross_origin()
def get_image(run, folder, image):
    return service.get_file(run, folder, image)


@app.route("/delete", methods=['POST'])
@cross_origin()
def delete_images():
    service.delete_files(request.json)
    return jsonify("Deleted")


@app.route("/runs")
@cross_origin()
def get_runs():
    return jsonify(service.get_runs())


@app.route("/folder/<string:run>")
@cross_origin()
def get_folders_by_run(run):
    return jsonify(list(service.get_folders_by_run(run)))


@app.route("/images", methods=['POST'])
@cross_origin()
def get_image_names():
    return jsonify(list(service.get_image_names(request.json)))


@app.route("/move", methods=['POST'])
@cross_origin()
def move():
    service.move(request.json)
    return Response(status=200)


if __name__ == '__main__':
    pass

# set FLASK_APP=api.py
# flask run
