#!/usr/bin/env python

'''
Copyright (c) 2015, Mark Silliman
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# A very basic TurtleBot script that moves TurtleBot forward indefinitely. Press CTRL + C to stop.  To run:
# On TurtleBot:
# roslaunch turtlebot_bringup minimal.launch
# On work station:
# python goforward.py

import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

global init_pose
global curr_pose
#init_pose =[0,0,0]
global i
i= 0

def callback(data):
	global i
	global init_pose
	global curr_pose
	q0 = data.pose.pose.orientation.x
	q1 = data.pose.pose.orientation.y
	q2 = data.pose.pose.orientation.z
	q3 = data.pose.pose.orientation.w
	theta = math.atan2(2*(q0*q1+q2*q3),1-2*(q1*q1+q2*q2))

	if i == 0:
	    init_pose = [data.pose.pose.position.x,data.pose.pose.position.y,theta]
	    curr_pose = [data.pose.pose.position.x,data.pose.pose.position.y,theta]
	else:
	    curr_pose = [data.pose.pose.position.x,data.pose.pose.position.y,theta]
	#print("i is "+str(i))
	#print("current pose is " + str(curr_pose))
	i = i+1
class GoForward():
    def __init__(self, goal_pose=[7,6,0]):
	
	global init_pose
	global curr_pose
        # initiliaze
	print "Going Forward"
	self.pose=rospy.Subscriber('odom',Odometry, callback)
        rospy.on_shutdown(self.shutdown)
        
        self.cmd_vel = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)

	#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(10);
	print "I stopped?"
        # Twist is a datatype for velocity
        move_cmd = Twist()
	# let's go forward at 0.2 m/s
        move_cmd.linear.x = 0.2
	# let's turn at 0 radians/s
	move_cmd.angular.z = 0
	print ("goal pose is "+ str(goal_pose))
	rospy.sleep(1)
		
        while not rospy.is_shutdown():
	    dist_to_go = abs(goal_pose[0]-curr_pose[0]+goal_pose[1]-curr_pose[1])
	    #print ("distance to go is " + str(dist_to_go))
	    #if (dist_to_go<0):
		#move_cmd.linear.x = -0.2
	    if (abs(dist_to_go)>0.05):
        	self.cmd_vel.publish(move_cmd)
	    	# wait for 0.1 seconds (10 HZ) and publish again
            	r.sleep()
	    elif (abs(dist_to_go)<0.05):
		self.cmd_vel.publish(Twist())
		#print "done going forward"
		return
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)

class RotateToward():
    def __init__(self, goal_pose=[8,8,0]):
	global init_pose
	global curr_pose
        # initiliaze
	print "Turning"
	#rospy.loginfo("current pose is " + str(curr_pose))
        #rospy.init_node('Rotate', anonymous=False)

	self.truepose=rospy.Subscriber('odom',Odometry, callback)
        rospy.on_shutdown(self.shutdown)
        
        self.cmd_vel = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)

	#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(10);

        # Twist is a datatype for velocity
	angularspeed = 0.2
        move_cmd = Twist()
        move_cmd.linear.z = 0
	move_cmd.angular.z = angularspeed
	print ("goal pose is "+ str(goal_pose))
	#curr_pose = goal_pose
	#print ("current pose is "+ str(curr_pose))
	#print str(init_pose)
	# as long as you haven't ctrl + c keeping doing...
	#rospy.loginfo(type(curr_pose))
	#while(type(curr_pose)==None):
	#print curr_pose
	rospy.sleep(1)
	angle_to_go = (math.atan2(goal_pose[1]-curr_pose[1],goal_pose[0]-curr_pose[0]))-curr_pose[2]

	#rospy.loginfo("angle to go is " + str(angle_to_go))
	if (angle_to_go<0):
		#rospy.loginfo("ok going negative")
		move_cmd.angular.z = -angularspeed
        while not rospy.is_shutdown():
	    angle_to_go = (math.atan2(goal_pose[1]-curr_pose[1],goal_pose[0]-curr_pose[0]))-curr_pose[2]
	    #rospy.loginfo("angle to go is " + str(angle_to_go))
	    if (abs(angle_to_go)>0.15):
        	if (angle_to_go<0):
			#rospy.loginfo("ok going negative")
			move_cmd.angular.z = -angularspeed*5
		else:
			move_cmd.angular.z = -angularspeed*5
		self.cmd_vel.publish(move_cmd)
	    	# wait for 0.1 seconds (10 HZ) and publish again
            	r.sleep()
	    
	    elif (abs(angle_to_go)>0.03):
		if (angle_to_go<0):
			#rospy.loginfo("ok going negative")
			move_cmd.angular.z = -angularspeed
		else:
			move_cmd.angular.z = -angularspeed
		self.cmd_vel.publish(move_cmd)
	    	# wait for 0.1 seconds (10 HZ) and publish again
            	r.sleep()
	    
	    elif (abs(angle_to_go)<0.03):
		self.cmd_vel.publish(Twist())
		#print "done turning"
		return
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)
class RotateToDegree():
    def __init__(self, goal_angle=0):
	global init_pose
	global curr_pose
        # initiliaze
	print "Turning"
	#rospy.loginfo("current pose is " + str(curr_pose))
        #rospy.init_node('Rotate', anonymous=False)

	self.truepose=rospy.Subscriber('odom',Odometry, callback)
        rospy.on_shutdown(self.shutdown)
        
        self.cmd_vel = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)

	#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(10);

        # Twist is a datatype for velocity
	angularspeed = 0.2
        move_cmd = Twist()
        move_cmd.linear.z = 0
	move_cmd.angular.z = angularspeed
	#print ("goal pose is "+ str(goal_pose))
	#curr_pose = goal_pose
	#print ("current pose is "+ str(curr_pose))
	#print str(init_pose)
	# as long as you haven't ctrl + c keeping doing...
	#rospy.loginfo(type(curr_pose))
	#while(type(curr_pose)==None):
	#print curr_pose
	rospy.sleep(1)
	angle_to_go = math.radians(goal_angle)-curr_pose[2]
	print "hi"
	#rospy.loginfo("angle to go is " + str(angle_to_go))
	if (angle_to_go<0):
		#rospy.loginfo("ok going negative")
		move_cmd.angular.z = -angularspeed
        while not rospy.is_shutdown():
	    angle_to_go = math.radians(goal_angle)-curr_pose[2]
	    #rospy.loginfo("angle to go is " + str(angle_to_go))
	    if (abs(angle_to_go)>0.15):
        	if (angle_to_go<0):
			#rospy.loginfo("ok going negative")
			move_cmd.angular.z = -angularspeed*5
		else:
			move_cmd.angular.z = -angularspeed*5
		self.cmd_vel.publish(move_cmd)
	    	# wait for 0.1 seconds (10 HZ) and publish again
            	r.sleep()
	    
	    elif (abs(angle_to_go)>0.03):
		if (angle_to_go<0):
			#rospy.loginfo("ok going negative")
			move_cmd.angular.z = -angularspeed
		else:
			move_cmd.angular.z = -angularspeed
		self.cmd_vel.publish(move_cmd)
	    	# wait for 0.1 seconds (10 HZ) and publish again
            	r.sleep()
	    
	    elif (abs(angle_to_go)<0.03):
		self.cmd_vel.publish(Twist())
		#print "done turning"
		return
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)
if __name__ == '__main__':
    try:
	rospy.init_node('GoForward', anonymous=False)
	"""
	GoForward([6])
	rospy.sleep(5)
	print "sleeping"
	GoForward([7])
	rospy.sleep(5)
        GoForward([8])
	rospy.sleep(5)
	GoForward([9])
	"""
	#GoForward()

	Pose1= [5,5,0]
	Pose1 = input("input pose: ")
	RotateToDegree(Pose1)
	#rospy.sleep(1)
	#GoForward(Pose1)
	
	#Pose2 = [7,10,0]
	#rospy.sleep(2)
	#Rotate(Pose2)
	#rospy.sleep(1)
	#GoForward(Pose2)
    except:
        rospy.loginfo("GoForward node terminated.")

