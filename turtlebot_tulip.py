import rospy
import turtlescenario as ts
import goforward_turtlebot as tur
import detectobstacle as obs
import discrete_to_world_corr
#global obstacle_present
if __name__ == '__main__':
	#global obstacle_present
	try:
		rospy.init_node('Tulip_Controller', anonymous=False)
		mapping = discrete_to_world_corr.mapping
		tulipcontrol= ts.ctrl
		

		X1reach = True
		from_state = 'Sinit'
		while(1):
			input_val =X1reach #= input("input signal: ")
			inputs = {'X1reach': input_val, 'park' : 1}#input_val}
			retval = tulipcontrol.reaction(from_state,inputs)
			state = retval[1]['loc']
			print retval
			print state
			Pose = mapping[state]
			#print state
			from_state = retval[0];
			tur.Rotate(Pose)
			tur.rospy.sleep(0.5)
			tur.GoForward(Pose)
			#### HACK
			#tur.Rotate(mapping['X1'])
			#obstacle_present = False
			detect_obstacle = obs#.Detect()
			detect_obstacle.Detect(mapping['X1'])
			X1reach = detect_obstacle.obstacle_present
			print X1reach
		#Pose1= [5,5,0]
		#Pose1 = input("input pose: ")


		#Pose2 = [7,10,0]
		#rospy.sleep(2)
		#Rotate(Pose2)
		#rospy.sleep(1)
		#GoForward(Pose2)
	except:
		rospy.loginfo("GoForward node terminated.")
	
