#!/usr/bin/env python
__author__ = 'andrii.kudriashov@gmail.com'

import rospy
import math
import laser_geometry
import json
from numpy import arange
from sensor_msgs.msg import LaserScan
from time import sleep
import zmq
import sensor_msgs.point_cloud2 as pc2

# zmq_publisher settings
zmq_port = "5555"
zmq_context = zmq.Context()
print "Connecting to server..."
zmq_socket = zmq_context.socket(zmq.REQ)
zmq_socket.connect ("tcp://localhost:%s" % zmq_port)

geometry = laser_geometry.LaserProjection()


def generatemap(scan):
    mapa_pc2 = []
    cloud = geometry.projectLaser(scan_in=scan)
    gen = pc2.read_points(cloud, skip_nans=True, field_names=("x", "y", "z"))
    for point in gen:
        x, y, z = point
        mapa_pc2.append([x, y])

    return mapa_pc2


def callback(scan):
    # rospy.loginfo("some message")
    mapa = generatemap(scan)
    mapa_string = json.dumps(mapa)
    zmq_socket.send(mapa_string)
    message = zmq_socket.recv()
    print "received reply: ", message


def listener():
    rospy.init_node('listener_karmeluk')

    rospy.Subscriber("most_intense", LaserScan, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
