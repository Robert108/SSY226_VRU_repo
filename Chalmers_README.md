# Information

## How to set up the Raspberry pi to Collect measurements

First you need to install the Sense Hat and the adafruit GPS hat and connect the antenna.

To be able to collect data some configurations is needed to be done:
* Copy the script and then make it executable using chmod +x all_sensors.py
* Install nmea2 module using: pip install pynmea2
* In /boot/config.txt,  add dtoverlay=rpi-sense at the bottom of the file
* Go to Preferences>Raspberry Pi Configuration>I2C: Enable
* Type sudo raspi-config and Go to Localisation Options>Interfacting Options>Enable I2C

Now just run the script, you should see a red light as soon as you run the script and collect data by clicking the button(red light turns green).
To stop the measurements to be collected just press the button again and the led should go back to red. A new .csv file will now have been created in the same folder as the python script. Press the button again to create a new collection of measurements into a new file. The files are named after the time when they were created.

One notice! Dont put the end of the GPS antenna near the raspberry pi. This is since the end is magnetic and will destroy the magnetometer readings.



## The Orientation Filter
The orientation filter is implemented in Python and supposed to be run on the Raspberry Pi. This filter is calculating the orientation of the raspberry Pi which is used to generate the rotation matrix to rotate the accelerations into the world frame.

For the filter to run a number of files needs to be in the run directory:
* mu_g.py
* mu_m.py
* mu_normalizeQ.py
* OrientFilter.py
* quat2rotm.py
* Somega.py
* Sq.py
* tu_qw.py

The orientfilter is the main file that runs one iteration of the fileter. To see how it can be used, plase look at the example_main.py.

## Server
A server was set-up at a dedicated address by Ericsson. 

Simply connect to the server by typing:
* ssh student@40.113.6.77 
* The password is: elcity999
Note that the address and the password might be different for other users.

Just follow the instructions provided at the Readme.md file to run the connected bike demo. There were, however, a few errors that were encountered while attempting to do this, which is discussed in detail on the Error_Analysis.md file under the 'Server' section.
