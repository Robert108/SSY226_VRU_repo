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

class CollisionDetector:
    "Detects potenial collisions"

    def __init__(self, logger_handler, loglevel, send_warning_callback, send_intersection_info_callback, deltatime):
        self._time = datetime.datetime.now()
        self._group_a = {}
        self._group_b = {}
        self._sw = (57.40000, 11.570000)
        self._nw = (57.90000, 11.570000)
        self._ne = (57.90000, 13.05000)
        self._se = (57.40000, 13.05000)
        self._distance_between_sw_and_se = haversine(self._sw, self._se) * 1000
        self._distance_between_sw_and_nw = haversine(self._sw, self._nw) * 1000
        self._latitudal_conversion_factor = self._distance_between_sw_and_nw / (self._nw[0] - self._sw[0])
        self._longitudal_conversion_factor =  self._distance_between_sw_and_se / (self._se[1] - self._sw[1])
        self._logger = logging.Logger('Collision Detector')
        self._logger.addHandler(logger_handler)
        self._logger.setLevel(loglevel)
        self._send_warning = send_warning_callback
        self._send_intersection_info = send_intersection_info_callback
        self._deltatime = deltatime

    @property
    def sw(self):
        "sw"
        return self._sw

    @property
    def se(self):
        "se"
        return self._se

    @property
    def ne(self):
        "ne"
        return self._ne

    @property
    def nw(self):
        "nw"
        return self._nw

    @property
    def group_A(self):
        "List of vehicles in group A"
        return self._group_a

    @property
    def group_B(self):
        "List of vehicles in group B"
        return self._group_b

    def add_to_group_A(self, vehicle: Vehicle)  -> None:
        self._group_a[vehicle.id] = vehicle

    def add_to_group_B(self, vehicle: Vehicle)  -> None:
        self._group_b[vehicle.id] = vehicle

    def position_to_coordinate(self, position: Position):
        "Converts position into coordinate"
        y = (position.lat  - self._sw[0]) * self._latitudal_conversion_factor
        x = (position.lon - self._sw[1]) * self._longitudal_conversion_factor
        return (int(round(x)), int(round(y)))

    def coordinate_to_position(self, coordinate ):
        "Coordinate into position"
        position = Position()
        position.lat = coordinate[1]/self._latitudal_conversion_factor + self._sw[0]
        position.lon = coordinate[0]/self._longitudal_conversion_factor + self._sw[1]
        return position

    def coordinate_to_pos(self, coordinate ):
        "Coordinate into position"
        latitude = coordinate[1]/self._latitudal_conversion_factor + self._sw[0]
        longitude = coordinate[0]/self._longitudal_conversion_factor + self._sw[1]

        return {"lat":latitude, "lon":longitude}

    @asyncio.coroutine
    def monitor_vehicles(self, stale_position_time, projector_a, projector_b, loop):
        self._loop = loop
        """ Monitor vehicle positions and send out collision warnings """
        while True:
            self._logger.debug("Loop iteration")
            now = datetime.datetime.now(datetime.timezone.utc)
            stale_as = []
            for a_key, a in self._group_a.items() :
                if((now - a.cpos.time).total_seconds() > stale_position_time) :
                    stale_as.append(a_key)
                    continue

                stale_bs = []
                for b_key, b in self._group_b.items() :
                    if((now - b.cpos.time).total_seconds() > stale_position_time) :
                        stale_bs.append(b_key)
                        continue
                    distance = haversine((b.cpos.lat, b.cpos.lon), (a.cpos.lat, a.cpos.lon)) * 1000
                    if(distance < 100) :
                        projected_a_position = projector_a.projected_position(self._deltatime, int(round(a.cpos.course)), self.position_to_coordinate, a.cpos )
                        projected_b_position = projector_b.projected_position(self._deltatime, int(round(b.cpos.course)), self.position_to_coordinate, b.cpos)

                        a_exterior_positions = list(map(self.coordinate_to_pos, projected_a_position.polygon.exterior.coords))
                        a.projected_position = a_exterior_positions
                        debug_string = ""
                        for pos in a_exterior_positions:
                            debug_string +="{" + "lat: {0}, lng: {1}".format(pos["lat"], pos["lon"]) + "},"

                        self._logger.debug("a's projected position")
                        self._logger.debug(debug_string)

                        b_exterior_positions = list(map(self.coordinate_to_pos, projected_b_position.polygon.exterior.coords))
                        b.projected_position = b_exterior_positions
                        debug_string = ""
                        for pos in b_exterior_positions:
                            debug_string +="{" + "lat: {0}, lng: {1}".format(pos["lat"], pos["lon"]) + "},"

                        self._logger.debug("b's projected position")
                        self._logger.debug(debug_string)

                        if(projected_a_position.intersects(projected_b_position)) :
                            direction_to_b = projected_a_position.angle(projected_b_position)
                            direction_to_a = projected_b_position.angle(projected_a_position)
                            midpoint = self.coordinate_to_pos( projected_a_position.midpoint(projected_b_position))
                            self._logger.debug("There is an intersection")
                            self._send_warning(distance, direction_to_b,  b.id, a.id)
                            self._send_warning(distance, direction_to_a, a.id, b.id)
                            self._send_intersection_info(distance, midpoint, a, b)

                for key in stale_bs :
                    del self._group_b[key]

            for key in stale_as:
                del self._group_a[key]

            yield from asyncio.sleep(1, loop=self._loop)