 #!/usr/bin/env python

import rospy
import random
from std_msgs.msg import Float32

def talker():
    pub = rospy.Publisher('my_random_float', Float32)
    rospy.init_node('simple_publisher')
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        my_number = random.uniform(0.0, 10.0)
        rospy.loginfo(my_number)
        pub.publish(my_number)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass