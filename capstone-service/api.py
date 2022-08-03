import logging as log

from flask import *
from flask_cors import CORS

import annotator_service
import graph_generator_service
import stats_generator_service

app = Flask(__name__)
CORS(app)
log.getLogger('werkzeug').setLevel(log.ERROR)
app.config['JSON_SORT_KEYS'] = False


@app.route("/image/<string:run>/<string:folder>/<string:tracklet>/<string:image>")
def get_image(run, folder, tracklet, image):
    return make_response(annotator_service.get_compressed_image_file(run, folder, tracklet, image), 200)


@app.post("/delete")
def delete_tracklets():
    return Response(status=200) if annotator_service.delete_tracklets(request.json) else Response(status=400)


@app.route("/runs")
def get_runs():
    return jsonify(annotator_service.get_runs())


@app.post("/folders")
def get_folders_by_run():
    """ :returns: a folder to tracklets map"""
    return jsonify(annotator_service.get_folders_by_run(request.json))


@app.post("/tracklets-to-images")
def get_tracklets_to_image_names_map():
    """ :returns: tracklet to image names map """
    return jsonify(annotator_service.get_image_names(request.json))


@app.post("/merge")
def extract():
    """ :returns: the new folder name """
    return jsonify(annotator_service.extract_into_new_folder(request.json))


@app.post("/generate-stats")
def generate_stats():
    stats_generator_service.generate_stats(request.json)
    return jsonify(["generated"])


@app.get("/get-stats-by-interval")
def get_tickets_by_interval():
    return jsonify(stats_generator_service.get_tickets_by_interval())


@app.route("/service-time-graph")
def get_service_time_graph():
    return graph_generator_service.service_time_graph()


@app.route("/distribution-by-time-interval-graph")
def get_distribution_by_time_interval_graph():
    return graph_generator_service.distribution_by_time_interval_graph()


@app.route("/service-time-distribution-graph")
def get_service_time_distribution_graph():
    return graph_generator_service.service_time_distribution_graph()


if __name__ == '__main__':
    pass

# set FLASK_APP=api.py
# flask run
