#!/usr/bin/env python
__author__ = 'andrii.kudriashov@gmail.com'

import rospy
import math
# import laser_web

from numpy import arange
from sensor_msgs.msg import LaserScan
from time import sleep


def mapofsamples(scan):
    iterator = 0
    mapa = []
    for theta in arange(scan.angle_min, scan.angle_max, scan.angle_increment):
        x = scan.ranges[iterator] * math.cos(math.degrees(theta))
        y = scan.ranges[iterator] * math.sin(math.degrees(theta))
        # print "x: %s, y: %s" % (x,y)
        iterator += 1
        mapa.append([x,y])
        if iterator == 1080:
            return mapa


def callback(scan):
    # rospy.loginfo("ranges: " + str(scan.ranges))
    mapa = mapofsamples(scan)
    sleep(2)
    print mapa
    # TODO: add bridge with web-server


def listener():
    rospy.init_node('listener_karmeluk')

    rospy.Subscriber("most_intense", LaserScan, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
