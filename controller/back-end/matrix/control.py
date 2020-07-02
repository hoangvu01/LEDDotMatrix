import queue, json, threading
import datetime
from datetime import datetime

from matrix import app, LED
from flask import Flask, request, abort, jsonify
from flask_cors import cross_origin

@app.route("/")
def home():
    return "asdfasDF"

@app.route("/api/getDisplay", methods=["GET"])
def get_display_attrs():
    """ """
    response = jsonify(LED.led_attrs)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/api/setDisplay", methods=["POST"])
@cross_origin(origin='*', headers=['Content-Type'])
def set_display_attrs():
    """
        Set LED display attributes
        :param - request.json {<attr>:<value>}
    """
    app.logger.info("{} Request received: {}".format(datetime.now(), request.json))
    if not request.json:
        abort(400)
    LED.tasks.put(request.json)
    return request.json, 201

