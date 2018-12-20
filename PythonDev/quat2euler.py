# function that converts the quaterions in the state to euler angles

import numpy as np

def quat2euler(quaternion):
	q0 = quaternion[0,0]
	q1 = quaternion[1,0]
	q2 = quaternion[2,0]
	q3 = quaternion[3,0]

	a = np.arctan( (2 * (q0*q1 + q2*q3)) /  (1 - 2*(q1*q1 + q2*q2) ) )	
	b = np.arcsin(2 * (q0*q2 - q3*q1) )
	c = np.arctan( (2 * (q0*q3 + q1*q2)) /  (1 - 2*(q2*q2 + q3*q3) ) )	
	temp = 180/np.pi
	euler = np.transpose(np.array([[temp * a,temp * b,temp * c]]))

	return euler
