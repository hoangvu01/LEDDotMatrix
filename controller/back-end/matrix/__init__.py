from flask import Flask

from hardware.clock import Led

LED = Led()
app = Flask(__name__)
