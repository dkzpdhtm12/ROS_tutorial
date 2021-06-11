#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

def control_move(key_number, pub):
    if key_number == "y":
        print("left")
        pub.publish(String(key_number))
            
    elif key_number == "x":
        print("right")
        pub.publish(String(key_number))

    elif key_number == "z":
        print("run")
        pub.publish(String(key_number))
            
    else:
        print("error! end the program")
        exit()

rospy.init_node('test_node', anonymous=True)
pub = rospy.Publisher('/front', String, queue_size=10)

control_move(left = input())

rospy.spin()
