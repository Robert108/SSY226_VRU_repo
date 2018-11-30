from sense_hat import SenseHat
from datetime import datetime
from csv import writer 

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

with open('data.csv', 'wb') as f:
    data_writer = writer(f)
    data_writer.writerow(['gyro_x', 'gyro_y', 'gyro_z',
                          'acc_x', 'acc_y', 'acc_z',
                          'mag_x', 'mag_y' , 'mag_z'])
    while True:
        data = get_sense_data()
        data_writer.writerow(data)
