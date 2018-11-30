from vehicle import Vehicle
from dencity_bike.model.position import Position
import asyncio
import json
import datetime
import dateutil.parser
import pytz
from pytz import timezone
import logging


class PositionHandler:
    """Subscribe on positionData and update state"""

    def __init__(self, group_a, group_b, vehicle_type_a, vehicle_type_b,
        logger_handler, loglevel):
        self._group_a = group_a
        self.vehicle_type_a = vehicle_type_a
        self._group_b = group_b
        self.vehicle_type_b = vehicle_type_b
        self._logger = logging.Logger("Collision Detector")
        self._logger = logging.Logger("Position handler")
        self._logger.setLevel(loglevel)
        self._logger.addHandler(logger_handler)

    @asyncio.coroutine
    def parse_and_update_position(self, msg):
        """Parses a warning represented as a JSON string and displays it"""
        try:
            position = msg.data.decode()
            subject =  msg.subject
            vehicle_id = subject.split(".")[1]
            json_position = json.loads(position)

            position = Position()
            position.vehicle_type = json_position["vehicle_type"]
            position.lat = json_position["lat"]
            position.lon = json_position["lon"]
            position.speed = json_position["speed"]
            position.course = json_position["course"]
            if position.course == None:
                position.course = 0

            position.time = dateutil.parser.parse(json_position["time"])
            if position.time.tzinfo == None:
                position.time = position.time.replace(tzinfo=pytz.utc)

            vehicle = Vehicle(position, vehicle_id)

        except Exception as e:
            self._logger.warning(
                "Could not parse position data, message received: " +
                msg.data.decode() + "Exception: " + str(e))
            return

        if position.vehicle_type == self.vehicle_type_a:
            self._group_a[vehicle.id] = vehicle
        elif position.vehicle_type == self.vehicle_type_b:
            self._group_b[vehicle.id] = vehicle
