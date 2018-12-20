# Takes the gyroscope readins and calulates the quaternion speed

import numpy as np

def Somega(w):
	# The matrix S(omega)
	wx = w[0,0]
	wy = w[1,0]
	wz = w[2,0]

	S = np.array([[0, -wx, -wy, -wz], [wx, 0, wz, -wy], [wy, -wz, 0, wx],[wz, wy, -wx, 0]])

	return S
