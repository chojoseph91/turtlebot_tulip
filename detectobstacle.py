#!/usr/bin/env python
import roslib
import rospy
import math
import numpy as np
import matplotlib.pyplot as plt

from sensor_msgs.msg import LaserScan
import move_turtlebot as move
import discrete_to_world_corr as dc

global obstacle_present
global max_count
global count
global max_obstacle_distance
global obstacle_distance
global obstacle_angle
global obstacle_location
max_obstacle_distance = 1 #1 meter
obstacle_present = False
max_count = 10
count = 0
#retval = False
class DetectAtCoor:
	def __init__(self, coor = dc.mapping['X1']):
		global max_count
		global count
	    	self.scan = rospy.Subscriber("/scan",LaserScan,self.callback)
		r = rospy.Rate(10);
		rospy.on_shutdown(self.shutdown)
		
		move.RotateToward(coor)
		count = 0
		while not rospy.is_shutdown():
			if count > max_count:
				return
			r.sleep()
	def callback(self, data):
		global obstacle_present
		global max_count
		global count
		global max_obstacle_distance
		global obstacle_distance
		global obstacle_angle
		count = count + 1
		#rospy.loginfo("hi")	
		if count == max_count:
			#print data
			#print data.ranges
			#print len(data.ranges)
			#print len([value for value in data.ranges[:70] if math.isnan(value)])
			#print len([value for value in data.ranges[-70:] if math.isnan(value)])
			#print [value for value in data.ranges[int(640*(1/10)):int(640*(9/10))] if (not math.isnan(value) and (value<1))]
			data_of_interest = data.ranges[int(640.0*0.1):int(640.0*0.9)]
			data_of_interest_clean=[value for value in data_of_interest if (not math.isnan(value))]
			if len(data_of_interest_clean) == 0:
				obstacle_distance = 2*max_obstacle_distance
				obstacle_angle = 0
			else:
				obstacle_distance =  np.min(data_of_interest_clean)
				obstacle_angle = (data_of_interest.index(obstacle_distance)/640.0*0.8)*60.0-30.0
			rospy.loginfo(obstacle_distance)
			rospy.loginfo(obstacle_angle)		
			obstacle_present = (obstacle_distance<max_obstacle_distance)
			rospy.loginfo(obstacle_present)
	def shutdown(self):
		# stop turtlebot
		rospy.loginfo("Stop TurtleBot")
		# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
		rospy.sleep(1)
class DetectAtAngle:
	def __init__(self, angle = 0):
		global max_count
		global count

	    	self.scan = rospy.Subscriber("/scan",LaserScan,self.callback)
		r = rospy.Rate(10);
		rospy.on_shutdown(self.shutdown)
		
		move.RotateToDegree(angle)
		count = 0
		while not rospy.is_shutdown():
			if count > max_count:
				return
			r.sleep()
	def callback(self, data):
		global obstacle_present
		global max_count
		global count
		global max_obstacle_distance
		global obstacle_distance
		global obstacle_angle
		global obstacle_location
		count = count + 1
		#rospy.loginfo("hi")	
		if count == max_count:
			#print data
			#print data.ranges
			#print len(data.ranges)
			#print len([value for value in data.ranges[:70] if math.isnan(value)])
			#print len([value for value in data.ranges[-70:] if math.isnan(value)])
			#print [value for value in data.ranges[int(640*(1/10)):int(640*(9/10))] if (not math.isnan(value) and (value<1))]
			data_of_interest = data.ranges[int(640.0*0.1):int(640.0*0.9)]
			data_of_interest_clean=[value for value in data_of_interest if (not math.isnan(value))]
			if len(data_of_interest_clean) == 0:
				obstacle_distance = 2*max_obstacle_distance
				obstacle_angle = 0
			else:
				obstacle_distance =  np.min(data_of_interest_clean)
				obstacle_angle = (data_of_interest.index(obstacle_distance)/640.0*0.8)*60.0-30.0 #in degrees
				pose = move.curr_pose
				obstacle_location = [pose[0]+obstacle_distance*math.cos(math.radians(obstacle_angle)+pose[2]),pose[1]+obstacle_distance*math.sin(math.radians(obstacle_angle)+pose[2])]
				rospy.loginfo(obstacle_location)
				print pose
			
			rospy.loginfo(obstacle_distance)
			rospy.loginfo(obstacle_angle)		
			obstacle_present = (obstacle_distance<max_obstacle_distance)
			rospy.loginfo(obstacle_present)
	def shutdown(self):
		# stop turtlebot
		rospy.loginfo("Stop TurtleBot")
		# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
		rospy.sleep(1)
if __name__ == "__main__":
    try:
	rospy.init_node('sensor_listener', anonymous=True) #make node 
	#rospy.Subscriber('/mobile_base/events/button',ButtonEvent,buttonsensorprint)
	#rospy.Subscriber('/mobile_base/events/bumper', BumperEvent,bumpersensorprint)
    	#rospy.Subscriber("/scan",LaserScan,callback,20)
	#DetectAtCoor(dc.mapping['X2'])
	DetectAtAngle(45)
	#rospy.spin()
    except:
        rospy.loginfo("GoForward node terminated.")
