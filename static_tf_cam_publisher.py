#!/usr/bin/env python

import rospy
import tf2_ros
import geometry_msgs.msg


def talker():
    rospy.init_node('static_tf_cam_publisher')

    try:
        br = tf2_ros.StaticTransformBroadcaster()

        left_cam_transform = geometry_msgs.msg.TransformStamped()
        left_cam_transform.header.stamp = rospy.Time.now()
        left_cam_transform.header.frame_id = "base_link_gt"
        left_cam_transform.child_frame_id = "left_cam"

        left_cam_transform.transform.translation.x = -0.05
        left_cam_transform.transform.translation.y = 0.0
        left_cam_transform.transform.translation.z = 0.0

        left_cam_transform.transform.rotation.x = 0.0
        left_cam_transform.transform.rotation.y = 0.0
        left_cam_transform.transform.rotation.z = 0.0
        left_cam_transform.transform.rotation.w = 1.0

        right_cam_transform = geometry_msgs.msg.TransformStamped()
        right_cam_transform.header.stamp = rospy.Time.now()
        right_cam_transform.header.frame_id = "base_link_gt"
        right_cam_transform.child_frame_id = "right_cam"

        right_cam_transform.transform.translation.x = 0.05
        right_cam_transform.transform.translation.y = 0.0
        right_cam_transform.transform.translation.z = 0.0

        right_cam_transform.transform.rotation.x = 0.0
        right_cam_transform.transform.rotation.y = 0.0
        right_cam_transform.transform.rotation.z = 0.0
        right_cam_transform.transform.rotation.w = 1.0
        br.sendTransform([right_cam_transform, left_cam_transform])

        rospy.spin()
        print("sent")
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException,
            tf2_ros.ExtrapolationException):
        print('oop')


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
