import datetime
from shapely.geometry import Polygon
from shapely.geometry import LineString
from math import atan2,degrees
import numpy

class ProjectedPosition:
    "Represents a projected position by a polygon"

    def __init__(self, dt, points, direction):
        self._time = datetime.datetime.now()
        self._dt = dt
        self._polygon =  Polygon(points, [])
        self._direction = direction

    @property
    def time(self):
        "Time position was recorded. Datetime. Default: Now"
        return self._time

    @property
    def dt(self):
        "Time length into the future of the projection"
        return self._dt

    @property
    def vehicle_id(self):
        "Id of vehicle"
        return self.vehicle_id

    @property
    def polygon(self):
        "Projected Position"
        return self._polygon

    def intersects(self, other):
       "Returns true of intersection with other polygon"
       return self._polygon.intersects(other.polygon)

    def angle(self, other) :
        "Returns the bearing or angle to the other polygon"
        xy =  numpy.subtract(other.polygon.exterior.coords[0], self.polygon.exterior.coords[0])
        v = degrees(atan2(xy[0], xy[1]))

        if(v < 0) :
            v += 360

        relative_v = v - self._direction
        if(relative_v < 0) :
            relative_v += 360

        return relative_v

    def midpoint(self, other) :
        "Returns the midpoint between this and other projected position"
        coordinates = []
        coordinates.append(self.polygon.exterior.coords[0])
        coordinates.append(other.polygon.exterior.coords[0])
        centroid = LineString(coordinates).centroid
        return (centroid.xy[0][0], centroid.xy[1][0])
