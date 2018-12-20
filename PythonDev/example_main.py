# -------------------------------------------------------------------------------------------------------------------------
#
#	Python script that takes continous reading from the sensors and calls the Orientation filter to estimate the orientation
#
# --------------------------------------------------------------------------------------------------------------------------

# --- imports
import numpy as np
from sense_hat import SenseHat
from OrientFilter import *
from quat2rotm import *
from datetime import datetime
from quat2euler import * 


# --- User created functions

# Function that reads IMU data. 
# Set use_mag = 1  to collect magnetometer data.
def get_sense_data(use_mag = 0):
	sense_data = []
	# get the data for acc and gyro
	gyro = sense.get_gyroscope_raw()
	acc  = sense.get_accelerometer_raw()
    
    # save the gyro data
	sense_data.append(gyro['x'])
	sense_data.append(gyro['y'])
	sense_data.append(gyro['z'])

	# save the acceleraion data
	sense_data.append(acc['x'] * 9.82)
	sense_data.append(acc['y'] * 9.82)
	sense_data.append(acc['z'] * 9.82)


	# If magnetometer values is to be collected.
	if use_mag == 1 : 
		mag  = sense.get_compass_raw()
		sense_data.append(mag['x'])
		sense_data.append(mag['y'])
		sense_data.append(mag['z'])

	return sense_data


# Get the sampling time from the last sample
# Returns the  current time and the sampling time.
def get_time(old_time):
	now = datetime.now()
	new_time = seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
	dt = new_time - old_time
	
	return new_time, dt


# --- User created Vaiables

# input variables to init the filter.
Ydata = np.array([2,0.5,2,2,9.82])
xhat = np.transpose(np.array([[1,0,0,0]]))
Phat = np.identity(4)
lastGyrData = np.transpose(np.array([[0,0,0]]))
temp = 0
time = 0
dt = 0
old_acc = np.transpose(np.array([[0,0,9.82]]))

# Lowpass filter. Set other then 1 to get a filtered signal.
alpha = 1



# --- run the filter.

# init the sensehat
port = "/dev/serial0"
sense = SenseHat()
sense.clear()


# start to run the filter
while True:

	# get the new measurements 
	# the magnetometer is not used since the sampling frequency of 
	# the magnetometer is much smaller then in the other two sensors.
	return_value = get_sense_data()

	# get the current time and the sampling time
	time, dt = get_time(time)

	# create the acceleration vector.
	acc = np.transpose((np.array([[return_value[3],return_value[4],return_value[5]]])))
	yacc = old_acc + alpha * (acc - old_acc)


	Ydata_acc = np.array([1,0.5,yacc[0,0], yacc[1,0], yacc[2,0]])
	Ydata_gyr = np.array([2,0.5,return_value[0],return_value[1],return_value[2]])

	# update the filter, once with the accelerometer and once with the gyro
	xhat, Phat, lastGyrData  = OrientFilter(Ydata_acc, xhat, Phat, lastGyrData, dt)
	xhat, Phat, lastGyrData  = OrientFilter(Ydata_gyr, xhat, Phat, lastGyrData, dt)

	# save the accelerometer reading to be used later.
	old_Acc = yacc
	

	# get the new measurements, this time with the magnetometer.
	return_value = get_sense_data(use_mag = 1)

	# get the current time and the sampling time
	time, dt = get_time(time)



	acc = np.transpose((np.array([[return_value[3],return_value[4],return_value[5]]])))
	yacc = old_acc + alpha * (acc - old_acc)
	
	Ydata_acc = np.array([1,0.5,yacc[0,0], yacc[1,0], yacc[2,0]])
	Ydata_gyr = np.array([2,0.5,return_value[0],return_value[1],return_value[2]])
	Ydata_mag = np.array([3,0.5,return_value[6],return_value[7],return_value[8]])

	# update the filter, once with the accelerometer, once woth the gyro and once with the magnetometer.
	xhat, Phat, lastGyrData  = OrientFilter(Ydata_acc, xhat, Phat, lastGyrData, dt)
	xhat, Phat, lastGyrData  = OrientFilter(Ydata_gyr, xhat, Phat, lastGyrData, dt)
	xhat, Phat, lastGyrData  = OrientFilter(Ydata_mag, xhat, Phat, lastGyrData, dt)

	# save the accelerometer reading to be used later.
	old_Acc = yacc

	
	# print for debugging
	# prints the euler angles
	if temp % 5 == 0:
		print(quat2euler(xhat))
		print(dt)
	temp = temp +1
	

