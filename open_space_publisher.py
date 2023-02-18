#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32
from ros_exercises.msg import OpenSpace
from math import log


def callback(data):
    pub = rospy.Publisher('open_space', OpenSpace)
    max_distance = max(data.ranges)
    max_index = data.ranges.index(max_distance)

    my_message = OpenSpace()
    my_message.angle = (max_index - 200) * (1.0/300.0) * 3.14159265
    my_message.distance = max_distance

    # rospy.loginfo(my_message)
    pub.publish(my_message)


def simple_subscriber():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('open_space_publisher')

    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        rospy.Subscriber('fake_scan', LaserScan, callback)
        rate.sleep()
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    simple_subscriber()
