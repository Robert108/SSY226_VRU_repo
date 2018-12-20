# function for doing the magnetometer updatea of the filter

import numpy as np
from mu_g import * # to get Qq(x) and dQdq(x)

def  mu_m(x, P, mag, m0, Rm):


	# Get the prediction
	hx = np.matmul(np.transpose(Qq(x)), m0)

	# Get the Jacobians
	[Qq0, Qq1, Qq2, Qq3] = dQqdq(x)

	#Hx = [np.transpose(Qq0)*g0, np.transpose(Qq1)*g0, np.transpose(Qq2)*g0, np.transpose(Qq3) * g0]
	Hx_0 =  np.matmul(np.transpose(Qq0), m0)
	Hx_1 =  np.matmul(np.transpose(Qq1), m0)
	Hx_2 =  np.matmul(np.transpose(Qq2), m0)
	Hx_3 =  np.matmul(np.transpose(Qq3), m0)
	Hx = np.concatenate((Hx_0, Hx_1, Hx_2, Hx_3) , axis = 1)

	#S = Hx * P * np.transpose(Hx) + Ra # Calc the innovation covariance
	S = np.matmul(Hx, np.matmul(P,  np.transpose(Hx))) + Rm    

	#K = P * np.transpose(Hx)*np.linalg.inv(S) # Calc the Kalman gain
	K = np.matmul(P,  np.matmul(np.transpose(Hx), np.linalg.inv(S)))


	#x = x + K * (mag - hx) # Calc the update mean
	x = x + np.matmul(K, (mag-hx))


	#P = P - K * S * np.transpose(K) # Calc the update covariance
	P = P - np.matmul(K, np.matmul(S, np.transpose(K)))

	return x, P





