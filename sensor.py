#!/usr/bin/env python
import roslib
import rospy
import math
import numpy as np
import matplotlib.pyplot as plt
from nav_msgs.msg import Odometry

from kobuki_msgs.msg import BumperEvent, ButtonEvent
from sensor_msgs.msg import LaserScan
global c
global f
c=np.array([])
f=np.array([])
class Sensors:
	def __init__(self):
        
		self.but = rospy.Subscriber('/mobile_base/events/button',ButtonEvent,self.buttonsensorprint)
		self.bump = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent,self.bumpersensorprint)
	    	self.scan = rospy.Subscriber("/scan",LaserScan,self.laser_callback)
		self.pose=rospy.Subscriber('odom',Odometry, self.odom_callback)
		# Subscriber for the laser data
		#self.sub = rospy.Subscriber('base_scan', LaserScan, self.laser_callback)



		# Let the world know we're ready
		rospy.loginfo('Sensor node initialized')

	def bumpersensorprint(self, msg):
	    	print msg
		print msg.state
	def buttonsensorprint(self, msg):
	    	print msg
		print '\n'
	def odom_callback(self,data):
		#print data
		theta = math.atan2(2*(q0*q1+q2*q3),1-2*(q1*q1+q2*q2))
		print theta
		print '\n'
	def laser_callback(self, data):
		global c
		global f
		r = data.ranges
		r = [value for value in r if not math.isnan(value)]
		
		closest = min(r)
		tempc = np.append(c,closest)
		c = tempc
		farthest = max(r)
		tempf = np.append(f,farthest)
		f = tempf
		var_c = np.std(c)
		mean_c = np.mean(c)
		var_f = np.std(f)
		mean_f = np.mean(f)
		
		#print "current c is: " + str(closest)
		#print "variance of c is: "+ str(var_c)
		#print "mean of c is: " + str(mean_c)
		#print str(len(c))		
		
		#print "current f is: " + str(farthest)
		#print "variance of f is: "+ str(var_f)
		#print "mean of f is: " + str(mean_f)
		
		#print str(len(data.ranges)) 
		
		#print "angle_min is " + str(data.angle_min)
		#print "angle_max is " + str(data.angle_max)
		#print "angle_increment is " + str(data.angle_increment)
		#print "closest angle is: " + str(data.angle_min+data.angle_increment*data.ranges.index(closest))
		#print "farthest angle is: " + str(data.angle_min+data.angle_increment*data.ranges.index(farthest))
		#print data.ranges
		#print '\n'
		"""
		if len(f) == 50:
			print data
			print data.ranges
			print len(data.ranges)
			print r
			print len(r)
			print len([value for value in data.ranges[:70] if math.isnan(value)])
			print len([value for value in data.ranges[-70:] if math.isnan(value)])
			print np.mean([value for value in data.ranges[300:340] if not math.isnan(value)])
		"""	
		#	np.save('wall6',c)

if __name__ == "__main__":
	
	rospy.init_node('sensor_listener', anonymous=True) #make node 
	#rospy.Subscriber('/mobile_base/events/button',ButtonEvent,buttonsensorprint)
	#rospy.Subscriber('/mobile_base/events/bumper', BumperEvent,bumpersensorprint)
    	#rospy.Subscriber("/scan",LaserScan,callback,20)
	Sensors()
	rospy.spin()
