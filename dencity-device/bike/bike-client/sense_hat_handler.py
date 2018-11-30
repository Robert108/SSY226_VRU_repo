from pixel_symbols import PixelSymbols
from sense_hat import SenseHat


class SenseHatHandler:
    """Handler for Raspberry Pi Sense Hat, primarily providing access to the display"""

    def __init__(self, rotation=0):
        self._hat = SenseHat()
        self._hat.set_rotation(rotation)

    def display(self, pattern=PixelSymbols().BLANK):
        """Displays the given pattern (default blank)"""
        self._hat.set_pixels(pattern)

    def quick_scroll_message(self, message):
        self._hat.show_message(message, scroll_speed=0.03)
