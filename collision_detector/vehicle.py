from collections import deque
from dencity_bike.model.position import Position
from projected_position import ProjectedPosition
import datetime
"Represents a vehicle"
class Vehicle:

    def __init__(self, position:Position, id):
        self._cpos = position
        self._id = id
        self._projected_position = []

    @property
    def id(self):
        "vehicle id"
        return self._id

    @property
    def cpos(self):
        "Current position"
        return self._cpos

    @property
    def projected_position(self):
        "Current position"
        return self._projected_position

    @projected_position.setter
    def projected_position(self, value):
        self._projected_position = value


    @property
    def as_dict(self):
        data = {}
        data['vehicle_id'] = self.id
        data['position'] = self.cpos.as_dict
        data['projected_position'] = self._projected_position
        return data