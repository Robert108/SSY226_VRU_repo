import numpy as np

def  mu_g(x, P, yacc, Ra, g0):

    #Input
    #x = state prediction
    #P = covarinace prediction
    #yacc = accelerometer measurement
    #Ra = accelerometer noise covarinace
    #g0 = nominal gravity vector
    #Output
    #x = State update
    #P = Covariance update '''
	# Get the prediction
	hx = np.matmul(np.transpose(Qq(x)), g0)

	# Get the Jacobians
	[Qq0, Qq1, Qq2, Qq3] = dQqdq(x)

	#Hx = [np.transpose(Qq0)*g0, np.transpose(Qq1)*g0, np.transpose(Qq2)*g0, np.transpose(Qq3) * g0]
	Hx_0 =  np.matmul(np.transpose(Qq0), g0)
	Hx_1 =  np.matmul(np.transpose(Qq1), g0)
	Hx_2 =  np.matmul(np.transpose(Qq2), g0)
	Hx_3 =  np.matmul(np.transpose(Qq3), g0)
	Hx = np.concatenate((Hx_0, Hx_1, Hx_2, Hx_3) , axis = 1)


	#S = Hx * P * np.transpose(Hx) + Ra # Calc the innovation covariance
	S = np.matmul(Hx, np.matmul(P,  np.transpose(Hx))) + Ra

	#K = P * np.transpose(Hx)*np.linalg.inv(S) # Calc the Kalman gain
	K = np.matmul(P,  np.matmul(np.transpose(Hx), np.linalg.inv(S)))
	
	#x = x + K * (yacc - hx) # Calc the update mean
	x = x + np.matmul(K, (yacc-hx))

	#P = P - K * S * np.transpose(K) # Calc the update covariance
	P = P - np.matmul(K, np.matmul(S, np.transpose(K)))
	return x, P


def Qq(q):
	q0 = q[0,0]
	q1 = q[1,0]
	q2 = q[2,0]
	q3 = q[3,0]

	Q =np.array(  [[2*(q0*q0 + q1*q1) - 1,2*(q1*q2 - q0*q3)	, 2*(q1*q3 + q0*q2)],
       				[2*(q1*q2+q0*q3),	2*(q0*q0 + q2*q2)-1	, 2*(q2*q3 - q0*q1)],
       				[2*(q1*q3-q0*q2),  	2*(q2*q3+q0*q1),		 2*(q0*q0 + q3*q3) - 1]])

	return Q


def dQqdq(q):
	q0 = q[0,0]
	q1 = q[1,0]
	q2 = q[2,0]
	q3 = q[3,0]

	Q0 = 2 * np.array([[2 * q0, 		-q3, 	q2],
				  	[q3, 		2*q0, 	-q1],
				  	[-q2, 		q1, 		2*q0]])

	Q1 = 2 * np.array([[2 * q1,	 	q2,	 	q3],
				  	[q2, 		0,	 	-q0],
				  	[q3, 		q0, 		0]])

	Q2 = 2 * np.array([[0,	 		q1,	 	q0],
				  	[q1, 		2*q2,	 q3],
				  	[-q0, 		q3, 		0]])

	Q3= 2 * np.array([[0,	 		-q0,	 	q1],
				  	[q0, 		0,	 	q2],
				  	[q1, 		q2, 		2*q3]])

	return Q0,Q1,Q2,Q3









