import numpy as np
from tu_qw import *
from Somega import *
from mu_normalizeQ import *
from mu_g import *
from mu_m import *

def OrientFilter(Ydata, xhat, Phat,  lastGyrData, dT):


# FILTERTEMPLATE  Filter template
#
# This is a template function for how to collect and filter data
# sent from a smartphone live.  Calibration data for the
# accelerometer, gyroscope and magnetometer assumed available as
# structs with fields m (mean) and R (variance).
#
# The function returns xhat as an array of structs comprising t
# (timestamp), x (state), and P (state covariance) for each
# timestamp, and meas an array of structs comprising t (timestamp),
# acc (accelerometer measurements), gyr (gyroscope measurements),
# mag (magnetometer measurements), and orint (orientation quaternions
# from the phone).  Measurements not availabe are marked with NaNs.
#
# As you implement your own orientation estimate, it will be
# visualized in a simple illustration.  If the orientation estimate
# is checked in the Sensor Fusion app, it will be displayed in a
# separate view.
#
# Note that it is not necessary to provide inputs (calAcc, calGyr, calMag).

  ## Filter settings
  
  # Add your filter settings here.
	R_acc = np.diag([0.00044, 0.00036, 0.00028])
	R_gyr = np.diag([0.000053, 0.000011, 0.000015])
	R_mag = np.diag([0.258, 0.2442, 0.2155])
  
  
	#g0 = np.transpose([0.02, 0.02, 9.7])
	g0 = np.array([[0.02],[0.025],[9.6]])
    # Taken from a measurement when the phone is flat 
  # Todo: Set g0 to some standard if calibration is nonexistent. 
	#m0 = np.transpose([0, np.sqrt(0^2 + 5^2), -53]) 
	m0 = np.array([[0],[5],[-53]])
  
  # = [-66.9876708984375,-54.0655708312988,24.4852104187012]'
  # Todo Calc m0 from the initial GPS position
  
	Lm = np.linalg.norm(m0)  # Set magnetic field vector length
	alpha_m = 0.05 # Set alpha for the magnetic AR filter
	magOut = False
  
	T = dT # Set delta time 
	x = xhat
	P = Phat
        
  # Acceleromter
	if (Ydata[0] == 1) and (9 < np.linalg.norm(Ydata[2:5])) and (np.linalg.norm(Ydata[2:5]) < 11): 	
		acc    = np.transpose(np.array([Ydata[2:5]]))
		x, P = mu_g(x, P, acc, R_acc, g0)
		x, P = mu_normalizeQ(x, P)
  
  # Gyroscope
	if Ydata[0] == 2:  # Gyr measurements are available 
		gyr    = np.transpose(np.array([Ydata[2:5]]))
		x, P = tu_qw(x, P, gyr, T, R_gyr)        
		x, P = mu_normalizeQ(x, P)
		lastGyrData = gyr     
	else: 
		x, P = tu_qw(x, P, lastGyrData, T, R_gyr)
		x, P = mu_normalizeQ(x, P)
		gyr = None      
       
  # Magnetometer
	if Ydata[0] == 3:  # Mag measurements are available 
		mag  = np.transpose(np.array([Ydata[2:5]]))
		x, P = mu_normalizeQ(x, P)
		x, P = mu_m(x, P, mag, m0, R_mag)
		x, P = mu_normalizeQ(x, P)


	return x, P,  lastGyrData
