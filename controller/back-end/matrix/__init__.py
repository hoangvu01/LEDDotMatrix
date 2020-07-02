from flask import Flask
from flask_cors import CORS, cross_origin

from hardware.clock import Led

LED = Led()
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={
        r"/api/getDisplay" : {"origins" : '*'},
        r"/api/setDisplay" : {"origins" : '*'}
      })


