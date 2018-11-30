# Bike Client
Python application that runs on a Raspberry Pi to provide positioning data and display warnings to the bike rider.

## Client set-up guide
### Requirements
* Raspberry Pi 3 Model B+
* GPSD-compliant GPS
* SenseHat
### Raspberry Pi 

#### Initial preparations
Update packages \
`sudo apt-get update`
`sudo apt-get upgrade`

Install sense hat support \
`sudo apt-get install sense-hat`

Install gpsd support \
`sudo apt-get install gpsd gpsd-clients`

(Or, if gpsd cannot be found in the sources list)
```text
wget http://ftp.se.debian.org/debian/pool/main/g/gpsd/python-gps_3.16-4_armhf.deb
wget http://ftp.se.debian.org/debian/pool/main/g/gpsd/libgps22_3.16-4_armhf.deb
wget http://ftp.se.debian.org/debian/pool/main/g/gpsd/gpsd-clients_3.16-4_armhf.deb
wget http://ftp.se.debian.org/debian/pool/main/g/gpsd/gpsd_3.16-4_armhf.deb
dpkg --install libgps22_3.16-4_armhf.deb
dpkg --install gpsd_3.16-4_armhf.deb
dpkg --install python-gps_3.16-4_armhf.deb
dpkg --install gpsd-clients_3.16-4_armhf.deb
```

#### Required Python packages
(sense_hat and gps3 install with packages above)

`pip3 install asyncio-nats-client`
`pip3 install pyyaml`
`pip3 install gps3`
`pip3 install python-dateutil`

### Application installation

#### Install dencity-bike model package
In `python-packages/dencity-bike`:

`pip3 install .`

#### Register application for automatic startup

Open the `rc.local` startup script \
`sudo nano /etc/rc.local`

Add the following line above the `exit 0` statement \
`sudo su - pi -c "screen -dm -S bike-client <path-to-bike-client>/delayed_startup.sh"`

#### Update configuration

In `bike-client`, open `bike_client.yaml` and set the `nats-connection-string` to the correct value.

Also give the client a unique ID by changing the value for `vehicle-id`

#### Start application

To start the application, go to `bike-client` and run \
`python3 bike_client.py`

## Architecture and inner workings

### Application architecture

The application consists of a main `bike_client.py` class that runs the application and binds the different handlers together

`gpsd_handler.py` interacts with GPS devices via `gpsd`, and owns the position monitoring task

`nats_handler.py` publishes and subscribes to NATS messages, and owns the subscription task and other NATS-releated tasks

`warnings_handler.py` parses and displays warnings using the provided display

`sense_hat_handler.py` interacts with the LED display on the Sense Hat

### Cooperating tasks

The functionality is centered around the concept of "cooperating tasks", i.e. tasks that continuously pause themselves to allow other tasks to run.
The two main tasks running are the _position monitoring task_ and the _NATS subscription task_.

The __position monitoring task__ checks for new data from `gpsd` every 100ms. If there is position data, it will parse said data into a `Position` object and call for it to be sent to NATS.

The __NATS subscription task__ continuously checks for NATS messages and upon receiving one, send the data to the warnings handler for processing.

Both tasks try to pause themselves often, to allow other tasks to run.

### Configuration

The configuration data is stored in `bike_client.yaml` and is read by `configuration.py` into the `data` dictionary.

## Trounleshooting

### GPS data

#### 1: No GPS data, gpsmon spits out "$GPTXT,01,01,01,NMEA unknown msg*58"
This error is usually due to _terminal echo_ being enabled on the UBS-serial port used by the GPS device.

To fix this, do the following
1. Unplug the GPS
2. Prepare the command `sudo stty -F /dev/ttyACM0 -echo` in a terminal
3. Plug the GPS back in
4. Run the above command

(In theory it should be possible to run this command whenever, but the errors spat out by the GPS causes the command to hang instead)

#### 2: No GPS data, gpsmon show no data
Most likely a non-USB GPS is used and not found by gpsd.

To fix this, we recommend following the instructios at https://www.rs-online.com/designspark/add-gps-time-and-location-to-a-raspberry-pi-project
