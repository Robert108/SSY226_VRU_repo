# function that normalizes the state and covariance matrix

import numpy as np

def mu_normalizeQ(x, P):
	# MU_NORMALIZEQ Normalize the quaternion
	x = x / np.linalg.norm(x)
	if x[0,0] < 0 :
		x = -1 * x

	return x, P
