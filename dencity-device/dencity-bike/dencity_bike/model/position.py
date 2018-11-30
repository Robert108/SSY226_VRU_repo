import json
import datetime


class Position:
    "Represents a position report from a bike to the dencity-bike backend"

    def __init__(self):
        self._client_version = 0
        self._vehicle_type = "bicycle"
        self._time = datetime.datetime.now()
        self._lat = 0.0
        self._lon = 0.0
        self._speed = 0.0
        self._course = 0.0
        self._alt = 0.0
        self._climb = 0.0
        self._ept = 0.0
        self._epv = 0.0
        self._epx = 0.0
        self._epy = 0.0
        self._eps = 0.0

    @property
    def vehicle_type(self):
        "Type of vehicle. Default: 'bicycle'"
        return self._vehicle_type

    @vehicle_type.setter
    def vehicle_type(self, value):
        self._vehicle_type = value

    @property
    def client_version(self):
        "Numeric version of client. Default: 0"
        return self._client_version

    @client_version.setter
    def client_version(self, value):
        self._client_version = value

    @property
    def time(self):
        "Time position was recorded. Datetime. Default: Now"
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def lat(self):
        "Latitudinal position in degrees. Default: 0.0"
        return self._lat

    @lat.setter
    def lat(self, value):
        self._lat = value

    @property
    def lon(self):
        "Longitudinal position in degrees. Default: 0.0"
        return self._lon

    @lon.setter
    def lon(self, value):
        self._lon = value

    @property
    def speed(self):
        "Speed in meters per second. Default 0.0"
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def course(self):
        "Course in degrees from true north. Default 0.0"
        return self._course

    @course.setter
    def course(self, value):
        self._course = value

    @property
    def alt(self):
        "Altitude in meters. Default: 0.0"
        return self._alt

    @alt.setter
    def alt(self, value):
        self._alt = value

    @property
    def climb(self):
        "Ascend/descent in meters per second. Default: 0.0"
        return self._climb

    @climb.setter
    def climb(self, value):
        self._climb = value

    @property
    def ept(self):
        "Estimated time error in seconds. Default: 0.0"
        return self._ept

    @ept.setter
    def ept(self, value):
        self._ept = value

    @property
    def epx(self):
        "Longitude error in meters. Default: 0.0"
        return self._epx

    @epx.setter
    def epx(self, value):
        self._epx = value

    @property
    def epy(self):
        "Latitude error in meters. Default: 0.0"
        return self._epy

    @epy.setter
    def epy(self, value):
        self._epy = value

    @property
    def epv(self):
        "Altitude error in meters. Default: 0.0"
        return self._epv

    @epv.setter
    def epv(self, value):
        self._epv = value

    @property
    def eps(self):
        "Speed error in meters. Default: 0.0"
        return self._eps

    @eps.setter
    def eps(self, value):
        self._eps = value

    @property
    def as_json(self):
        return json.dumps(self.as_dict)

    @property
    def as_dict(self):
        data = {}
        data['vehicle_type'] = self.vehicle_type
        data['client_version'] = self.client_version
        data['time'] = self.time.isoformat()
        data['lat'] = self.lat
        data['lon'] = self.lon
        data['speed'] = self.speed
        data['course'] = self.course
        data['alt'] = self.alt
        data['climb'] = self.climb
        data['ept'] = self.ept
        data['epv'] = self.epv
        data['epx'] = self.epx
        data['epy'] = self.epy
        data['eps'] = self.eps
        return data
