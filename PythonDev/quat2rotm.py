# Function that return the Orientation matrix from the guaterions 

import numpy as np

def quat2rotm(quaternion):

	qr = quaternion[0,0]
	qi = quaternion[1,0]
	qj = quaternion[2,0]
	qk = quaternion[3,0]

	R = np.array([[1 - 2*(qj*qj + qk*qk),		2*(qi*qj - qk*qr),		2*(qi*qk + qj*qr)],
				[2*(qi*qj + qk*qr),			1- 2*(qi*qi + qk*qk),	2*(qj*qk - qi*qr)],
				[2*(qi*qk - qj*qr),			2*(qj*qk + qi*qr),		1-2*(qi*qi + qj*qj)]])

	return R
	
