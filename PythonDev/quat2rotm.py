import numpy as np

#def quat2rotm(quaternion):

 #   EPS = np.finfo(float).eps * 4.0 # epsilon for testing whether a number is close to zero

    #q = np.array(quaternion, dtype=np.float64, copy=True)
    #print(q)
    #n = np.dot(q, q)
#    if n < EPS:
#        return numpy.identity(4)
#    q *= math.sqrt(2.0 / n)
#    q = np.outer(q, q)
#    rotm = np.array([
#        [1.0-q[2, 2]-q[3, 3],     q[1, 2]-q[3, 0],     q[1, 3]+q[2, 0], 0.0],
#        [    q[1, 2]+q[3, 0], 1.0-q[1, 1]-q[3, 3],     q[2, 3]-q[1, 0], 0.0],
#        [    q[1, 3]-q[2, 0],     q[2, 3]+q[1, 0], 1.0-q[1, 1]-q[2, 2], 0.0],
#        [                0.0,                 0.0,                 0.0, 1.0]])
#    return rotm


def quat2rotm(quaternion):

	qr = quaternion[0,0]
	qi = quaternion[1,0]
	qj = quaternion[2,0]
	qk = quaternion[3,0]

	R = np.array([[1 - 2*(qj*qj + qk*qk),		2*(qi*qj - qk*qr),		2*(qi*qk + qj*qr)],
				[2*(qi*qj + qk*qr),			1- 2*(qi*qi + qk*qk),	2*(qj*qk - qi*qr)],
				[2*(qi*qk - qj*qr),			2*(qj*qk + qi*qr),		1-2*(qi*qi + qj*qj)]])

	return R
	
