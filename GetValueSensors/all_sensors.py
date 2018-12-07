import serial
import pynmea2
from sense_hat import SenseHat
from datetime import datetime
from csv import writer 
import sys

port = "/dev/serial0"
temp = 1000000
sense = SenseHat()
sense.clear()

def get_sense_data():
    sense_data = []
    gyro = sense.get_gyroscope_raw()
    acc  = sense.get_accelerometer_raw()
    mag  = sense.get_compass_raw()
    
    sense_data.append(gyro['x'])
    sense_data.append(gyro['y'])
    sense_data.append(gyro['z'])

    sense_data.append(acc['x'])
    sense_data.append(acc['y'])
    sense_data.append(acc['z'])

    sense_data.append(mag['x'])
    sense_data.append(mag['y'])
    sense_data.append(mag['z'])

    return sense_data

def parseGPS(str_raw):
    print(str_raw)
    if str_raw.find('GGA') > 0:
        msg = pynmea2.parse(str_raw)
        print(msg)
        return (True , msg)
    return (False, str_raw)
     


def start_stop(run):
	for event in sense.stick.get_events():
		if event.action == "pressed":
			return not run

	return run

serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.5)
run = False
file_index = 1
sense.set_pixel(0,0,(255,0,0))
while True:
	run = start_stop(run)
	if run :
		sense.set_pixel(0,0,(0,255,0))
		with open('data_log_' + str(datetime.now().date()) + '_' +  str(file_index) + '.csv', 'wb') as f:
			data_writer = writer(f)
			while True:
				currentTime = datetime.now().time()
				try:
					sData= get_sense_data()
					str_raw = serialPort.readline()
					data_writer.writerow(['GYRO', currentTime, sData[0], sData[1], sData[2]])
					data_writer.writerow(['ACC', currentTime,     sData[3], sData[4], sData[5]])
					data_writer.writerow(['MAG', currentTime ,   sData[6], sData[7], sData[8]])
				except:
					sense.set_pixel(1,1,(255,0,0))
					fh = open("log.txt", "a")
					fh.write(str(sys.exc_info()) + "\n")
					continue
				return_data = parseGPS(str_raw)
				if return_data[0]:
					temp = temp - 1
					data = return_data[1]
					if data.lat == None or data.lon == None or data.altitude == None:
						pass
					else:
						data_writer.writerow(['GPS',currentTime, data.lat,data.lon,data.altitude])
					if temp == 0:
						break

				run = start_stop(run)
				if not run:
					break
			f.close()
			file_index = file_index + 1
			sense.set_pixel(0,0,(255,0,0))


			

    
