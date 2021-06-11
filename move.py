#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

laser_range = [None] * 721
laser_range[360] = 1.0
left_before = 0.0
right_before = 0.0
count_left = 0
count_right = 0

def control_move(left, right, pub):
    if left > right:
        print("left")
        fr = "y"
        pub.publish(String(fr))
            
    elif left < right:
        print("right")
        fr = "x"
        pub.publish(String(fr))
            
    else:
        fr = "z"
        pub.publish(String(fr))
        print('run')

def change_value(left,right):
    global left_before
    left_before = left
    global right_before 
    right_before = right

def callback(data):
    request_code = 0
    laser_input = data.ranges
    global count_left
    global count_right
    pub = rospy.Publisher('/front', String, queue_size=10)
    i = 0

    for laser_value in laser_input:
        if laser_value > 0:
            laser_range[i] = laser_value
            #if laser_range[i] > 0:
                #temp[i] = laser_range[i]
            i = i + 1
        else:
            i = i + 1
        #print(i, ' = ', laser_range[i])

    las = laser_range[329:389]
    las_left = laser_range[509:569]
    las_right = laser_range[149:209]

    left = min(las_left)
    right = min(las_right)

    if min(las) > 1.0 or min(las) == None:
        fr = "z"
        pub.publish(String(fr))
        print('run')
        
    else:
        request_code = 100

        if min(las_left) == left_before: 
            count_left = count_left + 1
        elif min(las_left) != left_before:
            count_left = 0

        if count_left >= 10:
            change_left_value = 10.0
        else:
            change_left_value = None

        if min(las_right) == right_before:
            count_right = count_right + 1
        elif min(las_right) != right_before:
            count_right = 0

        if count_right >= 10:
            change_right_value = 10.0
        else:
            change_right_value = None

    change_value(left, right)

    print(min(las), left, right, count_left, count_right)

    if request_code == 100:
        if change_left_value == 10.0 :
            control_move(change_left_value, right, pub)
        elif change_right_value == 10.0 :
            control_move(left, change_right_value, pub)
        elif change_right_value == 10.0 and change_left_value == 10.0:
            control_move(change_left_value, change_right_value, pub)
        else:
            control_move(left, right, pub)
        
        

rospy.init_node('ydlidar_node', anonymous=True)

sub = rospy.Subscriber("/scan", LaserScan, callback)
 
rospy.spin()
