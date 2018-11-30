import asyncio
import logging
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout


class NatsHandler:

    def __init__(self, connection_string, logger_handler, position_handler, nc=NATS(), loop=asyncio.get_event_loop()):
        self._connection_string = connection_string
        self.nc = nc
        self.loop = loop
        loop.set_debug(True)
        self._logger = logging.Logger('NATS')
        self._logger.addHandler(logger_handler)
        self._position_handler  = position_handler

    @asyncio.coroutine
    def on_message(self, msg):
        self._logger.debug("[Received on '{}']: {}".format(
            msg.subject, msg.data.decode()))
        task = self.loop.create_task(
            self._position_handler.parse_and_update_position(msg))
        yield from task

    @asyncio.coroutine
    def on_connect(self):
        self._logger.info("NATS reconnected '{}'".format(
            self.nc.connected_url.netloc))

    @asyncio.coroutine
    def on_error(self, exception):
        self._logger.info("Error raised '{}'".format(
            exception), exc_info=exception)

    @asyncio.coroutine
    def on_disconnect(self):
        self._logger.info("NATS disconnected")

    @asyncio.coroutine
    def on_close(self):
        self._logger.info("NATS closed")

    def connect(self):
        """Connects to NATS server, sets up subscription on warnings, and publishes a notification that it is online"""
        try:
            yield from self.nc.connect(
                io_loop=self.loop,
                servers=[self._connection_string],
                reconnected_cb=self.on_connect,
                error_cb=self.on_error,
                closed_cb=self.on_close,
                disconnected_cb=self.on_disconnect)
        except:
            self._logger.error("Error!")

        nc = self.nc
        self._logger.info("NATS connected '{}'".format(
            nc.connected_url.netloc))
        try:
            self.sid = yield from nc.subscribe("vehicle.*.position", cb=self.on_message)

        except ErrConnectionClosed:
            print("Connection closed prematurely")

        if nc.last_error is not None:
            print("Last Error: {}".format(nc.last_error))

        if nc.is_closed:
            print("Disconnected.")

        self._logger.debug("NATS subscription started")

        yield from nc.publish("collision_detector.status", b'Online!')

    def send_message(self, message, vehicle_id):
        """Sends a warning to vehicle"""
        self._logger.debug("message: " + message.as_json)
        encoded_message = message.as_json.encode('utf-8')
        self._logger.debug(encoded_message)

        subject = "vehicle." + str(vehicle_id) + ".warning"
        self._logger.debug("Sending message to NATS: " + subject)
        asyncio.ensure_future(self.nc.publish(subject, encoded_message), loop=self.loop)

    def send_intersection_info(self, message):
        """Sends intersection info to NATS"""
        self._logger.debug("message: " + message.as_json)
        encoded_message = message.as_json.encode('utf-8')
        self._logger.debug(encoded_message)

        subject = "collision_avoidance.warning"
        self._logger.debug("Sending message to NATS: " + subject)
        asyncio.ensure_future(self.nc.publish(subject, encoded_message), loop=self.loop)


    @asyncio.coroutine
    def async_close(self):
        self.loop.stop()
        self.loop.close()
        self.nc.close()

    def close(self):
        for task in asyncio.Task.all_tasks():
            task.cancel()
        asyncio.ensure_future(self.async_close())