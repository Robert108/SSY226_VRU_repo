#!/usr/bin/env python3
# coding=utf-8
"""
GPS3 (gps3.py) is a Python 2.7-3.5 GPSD interface (http://www.catb.org/gpsd)
Default host='127.0.0.1', port=2947, gpsd_protocol='json' in two classes.

1) 'GPSDSocket' creates a GPSD socket connection & request/retrieve GPSD output.
2) 'DataStream' Streamed gpsd JSON data literates it into python dictionaries.

Import          from gps3 import gps3
Instantiate     gpsd_socket = gps3.GPSDSocket()
                data_stream = gps3.DataStream()
Run             gpsd_socket.connect()
                gpsd_socket.watch()
Iterate         for new_data in gpsd_socket:
                    if new_data:
                        data_stream.unpack(new_data)
Use                     print('Altitude = ',data_stream.TPV['alt'])
                        print('Latitude = ',data_stream.TPV['lat'])

Consult Lines 144-ff for Attribute/Key possibilities.
or http://www.catb.org/gpsd/gpsd_json.html

Run human.py; python[X] human.py [arguments] for a human experience.
"""
from __future__ import print_function

import json
import select
import socket
import sys
from gps3 import gps3

class AltGPSDSocket(gps3.GPSDSocket):
    """Extends gps3 GPSDSocket to handle simultaneous messages, necessary on some platform/gps combinations"""

    def __init__(self):
        self.streamSock = None
        self.response = None
        self._gpsd_response = None
        super().__init__()

    def __iter__(self):
        """banana"""  # <--- for scale
        return self

    def next(self, timeout=0):
        if self._gpsd_response:
            self.response = self._gpsd_response.readline()

        if self.response:
            return self.response

        try:
            waitin, _waitout, _waiterror = select.select((self.streamSock,), (), (), timeout)
            if not waitin: return
            else:
                self._gpsd_response = self.streamSock.makefile()  # '.makefile(buffering=4096)' In strictly Python3
                self.response = self._gpsd_response.readline()
            return self.response

        except StopIteration as error:
            sys.stderr.write('The readline exception in GPSDSocket.next is--> {}'.format(error))

