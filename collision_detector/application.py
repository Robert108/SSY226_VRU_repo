from nats_handler import NatsHandler
from configuration import Configuration
from dencity_bike.model.warning import Warning
from collision_detector import CollisionDetector
from position_handler import PositionHandler
from vehicle import Vehicle
from intersection_info import IntersectionInfo
from projectors.vehicle_projector import VehiclePositionProjector
from projectors.person_projector import PersonPositionProjector
import atexit
import sys
import logging
import asyncio
import time
import yaml

try:
    from sense_hat_handler import SenseHatHandler
except ImportError:
    pass

class Appplication:
    """Main application class"""

    @property
    def COLLISION_DETECTOR_VERSION(self):
        "Collision detector version"
        return "1"

    def __init__(self):
        # Load configuration

        cfg = Configuration('config.yaml')
        self._cfg = cfg

        loglevel =  self._name_to_loglevel(cfg.data['loglevel'])
        self._configure_logger(loglevel)
        self._logger = logging.Logger("Application")

        deltatime = cfg.data['deltatime']
        vehicle_type_a = cfg.data['vehicle_type_a']
        vehicle_type_b = cfg.data['vehicle_type_b']


        # TODO: Figure out why this is necessary
        self._logger.addHandler(stdout)
        self._collision_detector = CollisionDetector(logger_handler=stdout, loglevel=loglevel, send_warning_callback=self.send_warning,
            send_intersection_info_callback=self.send_intersection_info, deltatime=deltatime)
        self._position_handler = PositionHandler(self._collision_detector._group_a, self._collision_detector._group_b, vehicle_type_a, vehicle_type_b, logger_handler=stdout, loglevel=loglevel)
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)

    def _name_to_loglevel (self, loglevel_name):
        if(loglevel_name == logging.getLevelName(logging.DEBUG)) :
            return logging.DEBUG
        else :
            return logging.INFO

    def _configure_logger(self, loglevel):
        root = logging.getLogger()
        root.setLevel(loglevel)

        global stdout
        stdout = logging.StreamHandler(sys.stdout)
        stdout.setLevel(loglevel)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stdout.setFormatter(formatter)
        # TODO: Why is it not enough to add the handler to the root logger??

        root.addHandler(stdout)

    def _get_position_projector(self, vehicle_type ):
        vehicle_type_to_projector = {
            "bus" : VehiclePositionProjector(),
            "bike" : VehiclePositionProjector(),
            "bicycle" : VehiclePositionProjector(),
            "car" : VehiclePositionProjector(),
            "smv" : VehiclePositionProjector(),
            "person" : PersonPositionProjector()
        }
        return vehicle_type_to_projector.get(vehicle_type)


    async def run(self):
        """Starts the application"""
        log = self._logger
        log.info("Starting collision_detector...")
        atexit.register(self.clean_up)  # Register clean-up

        cfg = self._cfg

        log.info("Configuration parsed " + yaml.dump(self._cfg.data))

        # Start NATS async IO
        nats = NatsHandler(
            cfg.data['nats-connection-string'],
            position_handler=self._position_handler,
            logger_handler=stdout,
            loop=self.loop)

        if cfg.data['nats-enabled']:
            nats_connect_task = self.loop.create_task(nats.connect())
        else:
            log.warning("NATS disabled in configuration")
        self._nats = nats

        # Register collision monitoring loop
        if cfg.data['collision_detector-enabled']:
            projector_a = self._get_position_projector(cfg.data['vehicle_type_a'])
            projector_b = self._get_position_projector(cfg.data['vehicle_type_b'])
            cd_task =  self.loop.create_task(self._collision_detector.monitor_vehicles(cfg.data["stale-position-time"], projector_a, projector_b, self.loop))
        else:
            log.warning("Collision detector disabled in configuration")

        await nats_connect_task
        await cd_task

    def clean_up(self):
        self._logger.info("Terminating the application")
        self._nats.close()
        self._logger.info("Termination complete")

    def send_warning(self, distance, direction, threat_id, vehicle_id):
        """Sends a collision warning to the intersecting vehicle, wraps it and sends it to NATS"""
        self._logger.debug("Send warning")
        message = Warning()
        message.threat_direction = direction
        message.threat_distance  = distance
        message.threat_identifier = threat_id

        self._nats.send_message(message, vehicle_id)

    def send_intersection_info(self, distance, midpoint, bus, bike):
        """Send intersection information"""
        self._logger.debug("Send intersection info")
        message = IntersectionInfo(distance, midpoint, bus, bike )


        self._nats.send_intersection_info(message)

if __name__ == "__main__":
    app = Appplication()
    app.loop.run_until_complete(app.run())