import queue, json, threading
import datetime
from datetime import datetime

from matrix import app, LED
from flask import Flask, request, abort

@app.route("/")
def home():
    return "asdfasDF"

@app.route("/api/getDisplay", methods=["GET"])
def get_display_attrs():
    """ """
    return json.dumps(LED.led_attrs)

@app.route("/api/setDisplay", methods=["POST"])
def set_display_attrs():
    """
        Set LED display attributes
        :param
    """
    app.logger.info("{} Request received: {}".format(datetime.now(), request.json))
    if not request.json:
        abort(400)
    LED.tasks.put(request.json)
    return request.json, 201

