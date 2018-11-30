from projected_position import ProjectedPosition
from collections import deque
import datetime
from vehicle import Vehicle
from haversine import haversine
from dencity_bike.model.position import Position
from shapely.geometry import Polygon
from shapely.affinity import rotate
from intersection_info import IntersectionInfo
import asyncio
import logging

class VehiclePositionProjector:
    "prjects vehicle position"

    def projected_position(self, dt, direction, position_to_coordinate_mapper, position) :
        "Calculates projected position of vehicle"
        SIN45 = 0.70710678118
        distance = position.speed * dt
        current_coordinate = position_to_coordinate_mapper(position)
        width = distance/2*SIN45
        points = []
        points.append(current_coordinate)
        points.append((current_coordinate[0] - width, current_coordinate[1] + width))
        points.append((current_coordinate[0] - width, current_coordinate[1] + distance))
        points.append((current_coordinate[0] + width, current_coordinate[1] + distance))
        points.append((current_coordinate[0] + width, current_coordinate[1] + width))
        polygon = Polygon(points, [])
        polygon=rotate(polygon, -direction, points[0])

        return ProjectedPosition(0, polygon, direction)