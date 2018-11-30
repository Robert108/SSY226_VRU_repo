from serial import Serial
import time
from pixel_symbols import PixelSymbols

class SparkFunHandler:
    """Handler for SparkFun Serial display"""

    def __init__(self, device):
        self._sparkfun = Serial(device, 9600)

    def display(self, pattern=PixelSymbols().BLANK):
        """Displays the given pattern (default blank)"""
        self._ensure_open()
        if pattern == PixelSymbols().BLANK:
            self._sparkfun.write(b"0,0,0")
        else:
            self._sparkfun.write(b"255,0,0")
        self._sparkfun.close()

    def quick_scroll_message(self, message):
        """Toggles an ouptut pin"""
        self._ensure_open()
        self._sparkfun.write(b"255,0,0")
        time.sleep(2)
        self._sparkfun.write(b"255,0,0")
        self._sparkfun.close()
        
    def _ensure_open(self):
        if self._sparkfun.is_open:
            return
        self._sparkfun.open()
        
if __name__ == "__main__":
    sparkfun =  Serial("/dev/ttyACM0", 9600)
    sparkfun.write(b'255,0,0')
    time.sleep(1.5)
    sparkfun.write(b'0,0,0')
    time.sleep(1.5)
    sparkfun.write(b'255,0,0')
    time.sleep(1.5)
    sparkfun.write(b'0,0,0')
    sparkfun.close()
    
    
