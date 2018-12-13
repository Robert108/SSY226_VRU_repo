import numpy as np
from sense_hat import SenseHat
from OrientFilter import *
from quat2rotm import *
from datetime import datetime
from quat2euler import * 

#import matplotlib.pyplot as plt

#t = np.arange(0.0, 2.0, 0.01)
#s = 1 + np.sin(2*np.pi*t)
#plt.plot(t, s)

#plt.xlabel('time (s)')
#plt.ylabel('voltage (mV)')
#plt.title('About as simple as it gets, folks')
#plt.grid(True)
#plt.savefig("test.png")
#plt.show()

def get_sense_data(use_mag = 0):
	sense_data = []
	gyro = sense.get_gyroscope_raw()
	acc  = sense.get_accelerometer_raw()
    
	sense_data.append(gyro['x'])
	sense_data.append(gyro['y'])
	sense_data.append(gyro['z'])

	sense_data.append(acc['x'] * 9.82)
	sense_data.append(acc['y'] * 9.82)
	sense_data.append(acc['z'] * 9.82)


	if use_mag == 1 : 
		mag  = sense.get_compass_raw()
		sense_data.append(mag['x'])
		sense_data.append(mag['y'])
		sense_data.append(mag['z'])

	return sense_data


def get_time(old_time):
	now = datetime.now()
	new_time = seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
	dt = new_time - old_time
	old_time = new_time
	
	return old_time, dt

Ydata = np.array([2,0.5,2,2,9.82])
xhat = np.transpose(np.array([[1,0,0,0]]))
Phat = np.identity(4)
lastGyrData = np.transpose(np.array([[0,0,0]]))

port = "/dev/serial0"
sense = SenseHat()
sense.clear()


#a,b,c = OrientFilter(Ydata, xhat, Phat,  lastGyrData, 0.5)



temp = 0
time = 0
dt = 0
old_acc = np.transpose(np.array([[0,0,9.82]]))
alpha = 1
RC = 0.1
while True:


	return_value = get_sense_data()
	time, dt = get_time(time)

	#alpha  = dt / (RC + dt)	
	acc = np.transpose((np.array([[return_value[3],return_value[4],return_value[5]]])))
	yacc = old_acc + alpha * (acc - old_acc)
	#print(alpha)

	Ydata_acc = np.array([1,0.5,yacc[0,0], yacc[1,0], yacc[2,0]])
	Ydata_gyr = np.array([2,0.5,return_value[0],return_value[1],return_value[2]])
	#Ydata_mag = np.array([3,0.5,return_value[6],return_value[7],return_value[8]])

	xhat, Phat, lastGyrData  = OrientFilter(Ydata_acc, xhat, Phat, lastGyrData, dt)
	xhat, Phat, lastGyrData  = OrientFilter(Ydata_gyr, xhat, Phat, lastGyrData, dt)
	#xhat, Phat, lastGyrData  = OrientFilter(Ydata_mag, xhat, Phat, lastGyrData, dt)

	old_Acc = yacc
	

	return_value = get_sense_data(use_mag = 1)
	time, dt = get_time(time)

	#alpha  = dt / (RC + dt)
	#print(alpha)	

	acc = np.transpose((np.array([[return_value[3],return_value[4],return_value[5]]])))
	yacc = old_acc + alpha * (acc - old_acc)
	
	Ydata_acc = np.array([1,0.5,yacc[0,0], yacc[1,0], yacc[2,0]])
	Ydata_gyr = np.array([2,0.5,return_value[0],return_value[1],return_value[2]])
	Ydata_mag = np.array([3,0.5,return_value[6],return_value[7],return_value[8]])

	xhat, Phat, lastGyrData  = OrientFilter(Ydata_acc, xhat, Phat, lastGyrData, dt)
	xhat, Phat, lastGyrData  = OrientFilter(Ydata_gyr, xhat, Phat, lastGyrData, dt)
	xhat, Phat, lastGyrData  = OrientFilter(Ydata_mag, xhat, Phat, lastGyrData, dt)

	old_Acc = yacc

	

	if temp % 1 == 0:
		#print(np.matmul(quat2rotm(xhat), acc))
		print(quat2euler(xhat))
		print(dt)
	temp = temp +1
	

