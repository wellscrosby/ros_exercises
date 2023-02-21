#!/usr/bin/env python

import rospy
import tf2_ros
import tf
import tf2_msgs.msg
from sensor_msgs.msg import LaserScan
import geometry_msgs.msg
import random
import math
import numpy as np


def talker():
    rospy.init_node('dynamic_tf_cam_publisher')

    # pub = rospy.Publisher('d', LaserScan)

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    rate = rospy.Rate(20)

    left_to_base = tf.transformations.identity_matrix()
    left_to_base[3][0] = -0.05
    # print(left_to_base)
    right_to_left = tf.transformations.identity_matrix()
    right_to_left[3][0] = 0.1

    while not rospy.is_shutdown():
        try:
            base_link_transform = tfBuffer.lookup_transform(
                "world", "base_link_gt", rospy.Time())
            # print("--------")
            # print(base_link_transform)
            # print(base_link_transform)

            base_link_transformation = tf.transformations.quaternion_matrix(
                [base_link_transform.transform.rotation.x,
                 base_link_transform.transform.rotation.y,
                 base_link_transform.transform.rotation.z,
                 base_link_transform.transform.rotation.w])

            base_link_transformation[0][3] = base_link_transform.transform.translation.x
            base_link_transformation[1][3] = base_link_transform.transform.translation.y
            base_link_transformation[2][3] = base_link_transform.transform.translation.z

            # left_cam_position = np.dot(base_link_transformation, [0.0, -0.05, 0.0, 1.0])
            # print(left_cam_position)
            left_cam_matrix = np.dot(base_link_transformation, left_to_base)

            # print('-----')
            # print("left_cam transformation matrix")
            # print(left_cam_matrix)

            # print("right_cam transformation matrix")
            # print(right_cam_matrix)
            # print(tf.transformations.translation_from_matrix(left_cam_matrix))

            br = tf.TransformBroadcaster()
            br.sendTransform(np.dot(base_link_transformation, [-0.05, 0.0, 0.0, 1.0]),
                             [base_link_transform.transform.rotation.x,
                              base_link_transform.transform.rotation.y,
                              base_link_transform.transform.rotation.z,
                              base_link_transform.transform.rotation.w],
                             rospy.Time.now(),
                             "left_cam",
                             "world")
            br.sendTransform([0.1, 0.0, 0.0],
                             [0.0, 0.0, 0.0, 1.0],
                             rospy.Time.now(),
                             "right_cam",
                             "left_cam")
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException,
                tf2_ros.ExtrapolationException):
            rate.sleep()
            print('oop')
            continue


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
