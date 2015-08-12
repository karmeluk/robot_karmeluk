#!/usr/bin/env python
__author__ = 'andrii.kudriashov@gmail.com'


import os
import sys

from flask import Flask, render_template, request
import zmq
from time import sleep
from threading import Thread
import json


class LaserListener(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self.zmq_port = "5555"
        self.zmq_context = zmq.Context()
        self.zmq_socket = self.zmq_context.socket(zmq.REP)
        self.zmq_socket.bind("tcp://*:%s" % self.zmq_port)

    def listen(self):
        mapa = self.zmq_socket.recv()
        print "received: ", mapa
        sleep(1)
        self.zmq_socket.send("from %s" % self.zmq_port)
        return mapa


ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../scripts")
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../scripts/templates")

app = Flask(__name__, static_folder=ASSETS_DIR, template_folder=TEMPLATE_DIR)
listener = LaserListener()
listener.start()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(chartID = 'chart_ID'):
    mapa = json.loads(listener.listen())
    # chart = {"renderTo": chartID}
    title = {"text": 'Robot Karmeluk'}
    subtitle = {"text": 'Laser Map'}
    xAxis = {"gridLineWidth": "1", "title": {"enabled": "true", "text": 'X ranges (cm)'},\
             "startOnTick": "true", "endOnTick": "true", "showLastLabel": "true"}
    yAxis = {"title": {"text": 'Y ranges (cm)'}}
    legend = {"layout": 'vertical', "align": 'right', "verticalAlign": 'middle'}
    series = [{"name": 'Observated ranges', "type": 'polygon', "data": mapa,\
               "color": 'yellow', "enableMouseTracking": 'false'}]
    tooltip = {"headerFormat": '<b>{series.name}</b><br>', "pointFormat": 'X:{point.x} cm, Y:{point.y} cm'}

    return render_template('index.html', chartID=chartID, title=title, subtitle=subtitle, xAxis=xAxis, yAxis=yAxis,\
                           legend=legend, series=series, tooltip=tooltip)

if __name__ == '__main__':
    app.run()
