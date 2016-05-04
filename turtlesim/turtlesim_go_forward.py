#!/usr/bin/env python


# Every python controller needs these lines
import roslib
import rospy
import math

# The velocity command message
from geometry_msgs.msg import Twist


# We use a hyperbolic tangent as a transfer function
from math import tanh

global distance
distance = 0.8
global hit
hit = 0

class Go_F:
    def __init__(self, max_speed=0.1, min_speed=0.01):
        # How close should we get to things, and what's our maximum speed?
        self.distance = distance
        self.max_speed = max_speed
        self.min_speed = min_speed

        # Publisher for movement commands
        self.pub = rospy.Publisher('/turtle1/cmd_vel', Twist,queue_size=10)

        # Let the world know we're ready
        rospy.loginfo('Stopper initialized')

    def go(self,speed = 0.1):

        command = Twist()
	command.linear.x = speed
        command.linear.y = 0.0
        command.linear.z = 0.0
        command.angular.x = 0.0
        command.angular.y = 0.0
        command.angular.z = 0.0
        
        # Send the command to the motors
        self.pub.publish(command)

if __name__ == '__main__':
    rospy.init_node('go')

    # Get the distance from the parameter server.  Default is 0.5
    #distance = rospy.get_param('distance', distance)

    # Set up the controller
    Go_F().go()

    # Hand control over to ROS
    rospy.spin()
