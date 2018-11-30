from pixel_symbols import PixelSymbols
from pifacedigitalio import PiFaceDigital
import time


class PiFaceHandler:
    """Handler for Raspberry Pi PiFace Digital 2, primarily providing access leds and pins"""

    def __init__(self, pin):
        self._piface = PiFaceDigital()
        self._pin = pin

    def display(self, pattern=PixelSymbols().BLANK):
        """Displays the given pattern (default blank)"""
        if pattern == PixelSymbols().BLANK:
            self._piface.output_pins[self._pin].turn_off()
            self._piface.output_pins[self._pin + 1].turn_off()
        else:
            self._piface.output_pins[self._pin].turn_on()
            self._piface.output_pins[self._pin + 1].turn_on()

    def quick_scroll_message(self, message):
        """Toggles an ouptut pin"""
        self._piface.output_pins[self._pin].turn_on()
        self._piface.output_pins[self._pin + 1].turn_on()
        time.sleep(0.5)
        self._piface.output_pins[self._pin].turn_off()
        self._piface.output_pins[self._pin + 1].turn_off()
        
