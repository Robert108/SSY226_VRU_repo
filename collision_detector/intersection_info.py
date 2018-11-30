import json
from dencity_bike.model.position import Position
from projected_position import ProjectedPosition
from vehicle import Vehicle
import datetime

class IntersectionInfo:
    "Represents an intersaction"
    def __init__(self, distance, midpoint, bus:Vehicle, bike:Vehicle):
        self._time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self._threat_distance =  distance
        self._priority = "medium"
        self._midpoint = midpoint
        self._bus = bus
        self._bike = bike

    @property
    def threat_distance(self):
        "Distance to threat in meters. Number. Default: 0.0"
        return self._threat_distance

    @threat_distance.setter
    def threat_distance(self, value):
        self._threat_distance = value

    @property
    def priority(self):
        "Priority of warning. Enum('high', 'medium', 'low'). Default: 'medium'"
        return self._priority

    @priority.setter
    def priority(self, value):
        self._priority = value

    @property
    def bus(self):
        "Bus"
        return self._bus

    @bus.setter
    def bus(self, value):
        self._bus = value

    @property
    def bike(self):
        "Bike"
        return self._bike

    @bike.setter
    def bike(self, value):
        self._bike = value

    @property
    def midpoint(self):
        "midpoint"
        return self._midpoint

    @midpoint.setter
    def midpoint(self, value):
        self._midpoint

    @property
    def time(self):
        "time"
        return self._time

    @time.setter
    def time(self, value):
        self._time

    @property
    def as_dict(self):
        data = {}
        data['time'] = self.time
        data['threat_distance'] = self.threat_distance
        data['threat_priority'] = self.priority
        data['bus'] = self._bus.as_dict
        data['bike'] = self._bike.as_dict
        data['midpoint'] = self._midpoint

        return data

    @property
    def as_json(self):
        return json.dumps(self.as_dict)