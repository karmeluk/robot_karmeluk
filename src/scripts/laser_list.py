#!/usr/bin/env python
__author__ = 'andrii.kudriashov@gmail.com'

import rospy
import math
# import laser_web
import json
from numpy import arange
from sensor_msgs.msg import LaserScan
from time import sleep
import zmq

# zmq_publisher settings
zmq_port = "5555"
zmq_context = zmq.Context()
print "Connecting to server..."
zmq_socket = zmq_context.socket(zmq.REQ)
zmq_socket.connect ("tcp://localhost:%s" % zmq_port)


def mapofsamples(scan):
    iterator = 0
    mapa = []
    for theta in arange(scan.angle_min, scan.angle_max, scan.angle_increment):
        x = scan.ranges[iterator] * math.cos(math.degrees(theta))
        y = scan.ranges[iterator] * math.sin(math.degrees(theta))
        # print "x: %s, y: %s" % (x,y)
        iterator += 1
        mapa.append([x,y])
        if iterator == 1081:
            for pair in mapa:
                pair[:] = [x * 100 for x in pair]
            return mapa


def callback(scan):
    # rospy.loginfo("ranges: " + str(scan.ranges))
    mapa = mapofsamples(scan)
    print mapa
    mapa_string = json.dumps(mapa)
    zmq_socket.send(mapa_string)
    sleep(1)
    message = zmq_socket.recv()
    print "received reply ", message


def listener():
    rospy.init_node('listener_karmeluk')

    rospy.Subscriber("most_intense", LaserScan, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
