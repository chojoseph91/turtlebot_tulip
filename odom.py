#!/usr/bin/env python
import roslib
import rospy
import math

from nav_msgs.msg import Odometry

def odometryCb(msg):
    	print msg.pose.pose
	print msg.twist.twist
	q0 = msg.pose.pose.orientation.x
	q1 = msg.pose.pose.orientation.y
	q2 = msg.pose.pose.orientation.z
	q3 = msg.pose.pose.orientation.w
	theta = math.atan2(2*(q0*q1+q2*q3),1-2*(q1*q1+q2*q2))
	print theta
	print '\n'

if __name__ == "__main__":
	rospy.init_node('odom_listener', anonymous=True) #make node 
	rospy.Subscriber('odom',Odometry,odometryCb)
	rospy.spin()
