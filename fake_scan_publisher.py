#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
import random
import math


def talker():
    pub = rospy.Publisher(rospy.get_param('/fake_scan_publish_topic', 'fake_scan'), LaserScan)
    rospy.init_node('fake_scan_publisher')
    rate = rospy.Rate(rospy.get_param('/fake_scan_publish_rate', 20))
    while not rospy.is_shutdown():
        fake_scan = LaserScan()

        fake_scan.header.stamp = rospy.Time.now()
        fake_scan.header.frame_id = 'base_link'
        fake_scan.angle_min = rospy.get_param('/fake_scan_angle_min', (-2.0/3.0) * 3.14159265)
        fake_scan.angle_max = rospy.get_param('/fake_scan_angle_max', (2.0/3.0) * 3.14159265)
        fake_scan.angle_increment = rospy.get_param('/fake_scan_angle_increment', (1.0/300.0) * 3.14159265)
        fake_scan.range_min = rospy.get_param('/fake_scan_range_min', 1.0)
        fake_scan.range_max = rospy.get_param('/fake_scan_range_max', 10.0)

        ranges_length = int(math.ceil(abs(fake_scan.angle_min - fake_scan.angle_max) / fake_scan.angle_increment))
        my_ranges = []
        for _ in range(0, ranges_length + 1):
            my_ranges.append(random.uniform(
                fake_scan.range_min, fake_scan.range_max))
        fake_scan.ranges = my_ranges
        pub.publish(fake_scan)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
