from projected_position import ProjectedPosition
from collections import deque
import datetime
from vehicle import Vehicle
from haversine import haversine
from dencity_bike.model.position import Position
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.affinity import rotate
from intersection_info import IntersectionInfo
import asyncio
import logging

class PersonPositionProjector:
    "prjects person position"

    def projected_position(self, dt, direction, position_to_coordinate_mapper, position) :
        "Calculates projected position of person"
        radius = 2 * dt
        current_coordinate = position_to_coordinate_mapper(position)
        circle =  Point(current_coordinate[0], current_coordinate[1]).buffer(radius)
        polygon = Polygon(circle, [])

        return ProjectedPosition(0, polygon, direction)