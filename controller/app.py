import queue

import clock
from clock import Led

from flask import Flask

app = Flask(__name__)

display = None

@app.route("/")
def home():
    return "asdfasDF"


@app.route("/display", methods=["GET", "POST", "PUT"])
def set_display_attrs():
    pass


if __name__ == "__main__":
    display = Led()
    app.run(host='0.0.0.0')

