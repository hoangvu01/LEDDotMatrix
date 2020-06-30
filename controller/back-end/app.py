import queue, json, threading

import datetime
from datetime import datetime

import clock
from clock import Led

from flask import Flask, request, abort

app = Flask(__name__)

display = None

@app.route("/")
def home():
    return "asdfasDF"

@app.route("/api/getDisplay", methods=["GET"])
def get_display_attrs():
    """ """
    return json.dumps(display.led_attrs)

@app.route("/api/setDisplay", methods=["POST"])
def set_display_attrs():
    """
        Set LED display attributes
        :param
    """
    if not request.json:
        app.logger.info("{} Request received: {}".format(datetime.now(), request))
        abort(400)
    display.tasks.put(request.json)
    return request.json, 201

if __name__ == "__main__":
    display = Led()

    led_thread = threading.Thread(target=display.run)
    app_thread = threading.Thread(target=app.run, kwargs={'host':'0.0.0.0'})

    led_thread.start()
    app_thread.start()

    led_thread.join()
    app_thread.join()

    app.run(host='0.0.0.0')

