#!/usr/bin/env python
import roslib
import rospy
import math
import numpy as np
import matplotlib.pyplot as plt

from kobuki_msgs.msg import BumperEvent, ButtonEvent
from sensor_msgs.msg import LaserScan
import goforward_turtlebot as gf
import discrete_to_world_corr as dc

global obstacle_present
global count
global retval
obstacle_present = False
count = 0
#retval = False
class Detect:
	def __init__(self, coor = dc.mapping['X1']):
        	global obstacle_present
		global count
		global retval
		self.but = rospy.Subscriber('/mobile_base/events/button',ButtonEvent,self.buttonsensorprint)
		self.bump = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent,self.bumpersensorprint)
	    	self.scan = rospy.Subscriber("/scan",LaserScan,self.callback)
		r = rospy.Rate(10);
		# Subscriber for the laser data
		#self.sub = rospy.Subscriber('base_scan', LaserScan, self.laser_callback)
		# Let the world know we're ready
		#rospy.loginfo('Sensor node initialized')
		rospy.on_shutdown(self.shutdown)
		
		gf.Rotate(coor)
		count = 0
		while not rospy.is_shutdown():
			if count >= 10:
				retval = obstacle_present
				#print obstacle_present
				return #obstacle_present
			#rospy.loginfo(count)
			r.sleep()
		#return obstacle_present

	def bumpersensorprint(self, msg):
	    	print msg
		print msg.state
	def buttonsensorprint(self, msg):
	    	print msg
		print '\n'
	def callback(self, data):
		global obstacle_present
		global count
		obstacle_distance = 1 # 1 meter
		count = count + 1
		#rospy.loginfo("hi")	
		if count == 10:
			#print data
			#print data.ranges
			#print len(data.ranges)
			#print len([value for value in data.ranges[:70] if math.isnan(value)])
			#print len([value for value in data.ranges[-70:] if math.isnan(value)])
			#print [value for value in data.ranges[int(640*(1/10)):int(640*(9/10))] if (not math.isnan(value) and (value<1))]
			closest_object =  np.mean([value for value in data.ranges[int(640.0*0.1):int(640.0*0.9)] if (not math.isnan(value) and (value<1))])
			rospy.loginfo(closest_object)			
			obstacle_present = (closest_object<obstacle_distance)
			print closest_object
			rospy.loginfo(obstacle_present)
			#return
	def shutdown(self):
		# stop turtlebot
		rospy.loginfo("Stop TurtleBot")
		# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
		rospy.sleep(1)
	def return_val(self):
		#global obstacle_present
		return True#obstacle_present
if __name__ == "__main__":
    try:
	rospy.init_node('sensor_listener', anonymous=True) #make node 
	#rospy.Subscriber('/mobile_base/events/button',ButtonEvent,buttonsensorprint)
	#rospy.Subscriber('/mobile_base/events/bumper', BumperEvent,bumpersensorprint)
    	#rospy.Subscriber("/scan",LaserScan,callback,20)
	Detect(dc.mapping['X5'])
	#rospy.spin()
    except:
        rospy.loginfo("GoForward node terminated.")
