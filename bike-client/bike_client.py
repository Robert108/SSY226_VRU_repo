from nats_handler import NatsHandler
from gpsd_handler import GpsHandler
from warnings_handler import WarningsHandler
from pixel_symbols import PixelSymbols, Colors
from configuration import Configuration
from dencity_bike.model.position import Position
from dencity_bike.model.warning import Warning
import atexit
import sys
import logging
import asyncio
import time

try:
    from sense_hat_handler import SenseHatHandler
except ImportError:
    pass

try:
    from piface_handler import PiFaceHandler
except ImportError:
    pass


class BikeClient:
    """Main application class"""

    @property
    def CLIENT_VERSION(self):
        "Client version"
        return "1"

    def __init__(self):
        self._configure_logger()
        self._logger = logging.Logger("Application")
        # TODO: Figure out why this is necessary
        self._logger.addHandler(stdout)
        self.loop = asyncio.get_event_loop()

    def _configure_logger(self):
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        global stdout
        stdout = logging.StreamHandler(sys.stdout)
        stdout.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stdout.setFormatter(formatter)
        # TODO: Why is it not enough to add the handler to the root logger??
        root.addHandler(stdout)

    def run(self):
        """Starts the application"""
        log = self._logger
        log.info("Starting bike_client...")
        atexit.register(self.clean_up)  # Register clean-up

        # Load configuration
        cfg = Configuration('bike_client.yaml')
        self._cfg = cfg

        log.info("Configuration parsed, vehicle ID is " +
                 cfg.data['vehicle-id'])

        if cfg.data['warnings-enabled']:
            # Configure display
            if cfg.data['display'] == 'sense-hat':
                display = SenseHatHandler(cfg.data['sense-hat-rotation'])
            elif cfg.data['display'] == 'piface':
                display = PiFaceHandler(cfg.data['piface-pin'])
            self._warnings_handler = WarningsHandler(display, cfg.data['stationary-speed'])
        else:
            log.info("Warnings disabled in configuration")
            display = None
            self._warnings_handler = None

        # Start NATS async IO
        nats = NatsHandler(
            cfg.data['nats-connection-string'],
            cfg.data['vehicle-id'],
            warnings_handler=self._warnings_handler,
            logger_handler=stdout,
            loop=self.loop)

        if cfg.data['nats-enabled']:
            nats.loop.run_until_complete(nats.connect())
        else:
            log.warning("NATS disabled in configuration")
        self._nats = nats

        # Register GPS monitoring loop
        gps = GpsHandler(
            logger_handler=stdout,
            use_alternate_gpslib=cfg.data['alternate-gps-lib'],
            gps_data_logging=cfg.data['gps-data-logging'])

        if cfg.data['gps-enabled']:
            asyncio.ensure_future(gps.monitor_positions(self))
        else:
            log.warning("GPS disabled in configuration")
        self._gps = gps

        # Optionally test Sense Hat
        if display is not None and cfg.data['test-sense-hat']:
            self._test_sense_hat()

        # Optionally test NATS
        if cfg.data['test-nats']:
            import dencity_bike.model.position as pos
            self.loop.call_soon(self.send_position, pos.Position())

        if display is not None and cfg.data['show-startup-message']:
            display.quick_scroll_message("ElectriCity")

        # Run the application main loop with all registered tasks
        self.loop.run_forever()

    def _test_sense_hat(self):
        display = SenseHatHandler()

        warning = Warning()
        WarningsHandler(display).display_warning(warning)

        warning.threat_direction = 90
        WarningsHandler(display).display_warning(warning)

        warning.threat_direction = 180
        WarningsHandler(display).display_warning(warning)

        warning.threat_direction = 270
        WarningsHandler(display).display_warning(warning)

    def clean_up(self):
        self._logger.info("Terminating the application")
        self._nats.close()
        self._logger.info("Termination complete")

    def send_position(self, position):
        """Receives a position from the GPS, updates it and sends it to NATS"""

        position.client_version = self.CLIENT_VERSION
        position.vehicle_type = self._cfg.data['vehicle-type']

        if self._cfg.data['warnings-enabled']:
            self._warnings_handler.current_speed = position.speed

        self._nats.send_message(position)


if __name__ == "__main__":
    app = BikeClient()
    app.run()
