from dencity_bike.model.warning import Warning
from pixel_symbols import PixelSymbols
from sense_hat_handler import SenseHatHandler
import asyncio
import json
import time


class WarningsHandler:
    "Displays warnings to the user"

    def __init__(self, display, stationary_speed=0.3):
        self._display = display
        self._last_threat_identifier = None
        self._last_threat_time = time.time()
        self._current_speed = 0.00
        self._stationary_speed = stationary_speed

    @property
    def current_speed(self):
        "Current vehicle speed"
        return self._current_speed


    @current_speed.setter
    def current_speed(self, value):
        self._current_speed = value

    @asyncio.coroutine
    def parse_and_display_warning(self, warning: str):
        """Parses a warning represented as a JSON string and displays it"""

        json_warning = json.loads(warning)

        warning = Warning()
        warning.type = json_warning['type']
        warning.priority = json_warning['threat_priority']
        warning.threat_direction = json_warning['threat_direction']
        warning.threat_distance = json_warning['threat_distance']
        warning.threat_identifier = json_warning['threat_identifier']

        if warning.threat_identifier == self._last_threat_identifier and (time.time() - self._last_threat_time) < 30:
            yield from asyncio.sleep(0.01)
        else:
            self._last_threat_identifier = warning.threat_identifier
            self._last_threat_time = time.time()
            yield from self.display_warning(warning)

    @asyncio.coroutine
    def display_warning(self, warning: Warning):
        """Displays the given warning"""

        pattern = self.from_direction(warning.threat_direction)

        led = self._display
        blank = PixelSymbols().BLANK
        led.display(pattern)
        yield from asyncio.sleep(0.1)
        led.display(blank)
        yield from asyncio.sleep(0.1)
        led.display(pattern)
        yield from asyncio.sleep(0.1)
        led.display(blank)
        yield from asyncio.sleep(0.1)
        led.display(pattern)
        yield from asyncio.sleep(4)
        led.display(blank)

    def from_direction(self, direction):
        if self._current_speed < self._stationary_speed:
            return PixelSymbols().WARNING_STATIONARY
        elif direction >= 315 or direction < 45:
            return PixelSymbols().WARNING_UP
        elif direction >= 45 and direction < 135:
            return PixelSymbols().WARNING_RIGHT
        elif direction >= 135 and direction < 225:
            return PixelSymbols().WARNING_DOWN
        else:
            return PixelSymbols().WARNING_LEFT
