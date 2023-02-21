#!/usr/bin/env python

import rospy
import tf2_ros
import tf
from sensor_msgs.msg import LaserScan
import geometry_msgs.msg
import numpy as np


def talker():
    rospy.init_node('dynamic_tf_cam_publisher')

    # pub = rospy.Publisher('d', LaserScan)

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    rate = rospy.Rate(20)

    left_to_base = tf.transformations.identity_matrix()
    left_to_base[0][3] = -0.05
    # print(left_to_base)
    right_to_left = tf.transformations.identity_matrix()
    right_to_left[0][3] = 0.1

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

            br = tf2_ros.TransformBroadcaster()

            left_cam_transform = geometry_msgs.msg.TransformStamped()
            left_cam_transform.header.stamp = rospy.Time.now()
            left_cam_transform.header.frame_id = "world"
            left_cam_transform.child_frame_id = "left_cam"

            left_cam_pos = np.dot(
                base_link_transformation, [-0.05, 0.0, 0.0, 1.0])

            left_cam_transform.transform.rotation = base_link_transform.transform.rotation

            left_cam_transform.transform.translation.x = left_cam_pos[0]
            left_cam_transform.transform.translation.y = left_cam_pos[1]
            left_cam_transform.transform.translation.z = left_cam_pos[2]

            right_cam_transform = geometry_msgs.msg.TransformStamped()
            right_cam_transform.header.stamp = rospy.Time.now()
            right_cam_transform.header.frame_id = "left_cam"
            right_cam_transform.child_frame_id = "right_cam"

            right_cam_transform.transform.translation.x = 0.1
            right_cam_transform.transform.translation.y = 0.0
            right_cam_transform.transform.translation.z = 0.0

            right_cam_transform.transform.rotation.x = 0.0
            right_cam_transform.transform.rotation.y = 0.0
            right_cam_transform.transform.rotation.z = 0.0
            right_cam_transform.transform.rotation.w = 1.0

            br.sendTransform([right_cam_transform, left_cam_transform])
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
