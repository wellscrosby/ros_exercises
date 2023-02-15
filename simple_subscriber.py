#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from math import log


def callback(data):
    pub = rospy.Publisher('random_float_log', Float32)
    ln_number = log(data.data)
    rospy.loginfo(ln_number)
    pub.publish(ln_number)


def simple_subscriber():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('simple_subscriber')

    rospy.Subscriber('my_random_float', Float32, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    simple_subscriber()
