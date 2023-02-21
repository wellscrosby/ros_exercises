#!/usr/bin/env python

import rospy
import tf
import tf2_ros
import geometry_msgs.msg
import numpy as np


def talker():
    rospy.init_node('base_link_tf_pub')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    base_to_left = tf.transformations.identity_matrix()
    base_to_left[0][3] = 0.05
    while not rospy.is_shutdown():
        try:

            br = tf2_ros.TransformBroadcaster()
            left_cam_transform = tfBuffer.lookup_transform(
                "world", "left_cam", rospy.Time())
            print("sent 1")
            left_cam_transformation = tf.transformations.quaternion_matrix(
                [left_cam_transform.transform.rotation.x,
                 left_cam_transform.transform.rotation.y,
                 left_cam_transform.transform.rotation.z,
                 left_cam_transform.transform.rotation.w])

            left_cam_transformation[0][3] = left_cam_transform.transform.translation.x
            left_cam_transformation[1][3] = left_cam_transform.transform.translation.y
            left_cam_transformation[2][3] = left_cam_transform.transform.translation.z

            base_link_gt_2_matrix = np.dot(
                left_cam_transformation, base_to_left)

            base_link_gt_2_transform = geometry_msgs.msg.TransformStamped()
            base_link_gt_2_transform.header.stamp = rospy.Time.now()
            base_link_gt_2_transform.header.frame_id = "world"
            base_link_gt_2_transform.child_frame_id = "base_link_gt_2"

            quat = tf.transformations.quaternion_from_matrix(
                base_link_gt_2_matrix)
            base_link_gt_2_transform.transform.rotation.x = quat[0]
            base_link_gt_2_transform.transform.rotation.y = quat[1]
            base_link_gt_2_transform.transform.rotation.z = quat[2]
            base_link_gt_2_transform.transform.rotation.w = quat[3]

            translation = tf.transformations.translation_from_matrix(
                base_link_gt_2_matrix)
            base_link_gt_2_transform.transform.translation.x = translation[0]
            base_link_gt_2_transform.transform.translation.y = translation[1]
            base_link_gt_2_transform.transform.translation.z = translation[2]

            br.sendTransform(base_link_gt_2_transform)
            print("sent")
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException,
                tf2_ros.ExtrapolationException):
            print('oop')


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
