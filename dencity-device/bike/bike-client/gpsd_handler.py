import dateutil.parser
import asyncio
from gps3 import gps3
from dencity_bike.model.position import Position
import logging


class GpsHandler:
    """Monitors GPSD for positions, creates Position objects and passes them on"""

    def __init__(self, logger_handler, use_alternate_gpslib=False, gps_data_logging=False):
        self._logger = logging.Logger('NATS')
        self._logger.addHandler(logger_handler)
        self._use_alternate_gpslib = use_alternate_gpslib
        self._last_position_time = None
        self._gps_data_logging = gps_data_logging

    def _ok(self, value):
        return value != 'n/a'

    async def monitor_positions(self, sender):
        """Starts the GPS position monitor loop"""

        # Initialize GPSD objects
        if(self._use_alternate_gpslib):
            from gps_alternate import AltGPSDSocket
            gps_socket = AltGPSDSocket()
        else:
            gps_socket = gps3.GPSDSocket()

        data = gps3.DataStream()

        # Start fetching data
        gps_socket.connect()
        gps_socket.watch()

        # Position monitor loop
        # for gps_data in gps_socket:
        while True:
            gps_data = gps_socket.next()
            if gps_data:  # We have data
                # Load the JSON into the mapping class dictionary
                data.unpack(gps_data)

                if self._gps_data_logging:
                    self._logger.debug("GPS Data: " + gps_data)

                #pylint: disable=E1101
                # (no, data.TPV doesn't exist in the code. yes, we can still call it)
                if self._ok(data.TPV['lat']):  # We have position data
                    gpos = data.TPV
                    pos = self.parsePosition(gpos)
                    if pos.time != self._last_position_time:
                        sender.send_position(pos)
                        self._last_position_time = pos.time

            await asyncio.sleep(0.1)

    def parsePosition(self, gpos):
        """Parses a GPSD TPV position into a position object"""
        pos = Position()

        # Values that always exist
        pos.lat = gpos['lat']
        pos.lon = gpos['lon']

        # Values that might not exist
        if self._ok(gpos['alt']):
            pos.alt = gpos['alt']
        if self._ok(gpos['track']):
            pos.course = gpos['track']
        if self._ok(gpos['climb']):
            pos.climb = gpos['climb']
        if self._ok(gpos['eps']):
            pos.eps = gpos['eps']
        if self._ok(gpos['epv']):
            pos.epv = gpos['epv']
        if self._ok(gpos['ept']):
            pos.ept = gpos['ept']
        if self._ok(gpos['epx']):
            pos.epx = gpos['epx']
        if self._ok(gpos['epy']):
            pos.epy = gpos['epy']
        if self._ok(gpos['speed']):
            pos.speed = gpos['speed']
        if self._ok(gpos['time']):
            pos.time = dateutil.parser.parse(gpos['time'])

        return pos
