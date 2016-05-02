import discrete
import goforward_sim as tur
import discrete_to_world_corr

if __name__ == '__main__':
	try:
		tur.rospy.init_node('GoForward', anonymous=False)
		mapping = discrete_to_world_corr.mapping
		tulipcontrol= discrete.ctrl
		


		from_state = 'Sinit'
		while(1):
			input_val = input("input signal: ")
			inputs = {'park' : input_val}
			retval = tulipcontrol.reaction(from_state,inputs)
			state = retval[1]['loc']
			print retval
			print state
			Pose = mapping[state]
			print state
			from_state = retval[0];
			tur.Rotate(Pose)
			tur.rospy.sleep(1)
			tur.GoForward(Pose)

		#Pose1= [5,5,0]
		#Pose1 = input("input pose: ")


		#Pose2 = [7,10,0]
		#rospy.sleep(2)
		#Rotate(Pose2)
		#rospy.sleep(1)
		#GoForward(Pose2)
	except:
		rospy.loginfo("GoForward node terminated.")
	
