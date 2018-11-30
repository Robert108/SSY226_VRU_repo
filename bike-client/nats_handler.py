import asyncio
import logging
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout


class NatsHandler:

    def __init__(self, connection_string, vehicle_id, logger_handler, warnings_handler, nc=NATS(), loop=asyncio.get_event_loop()):
        self._connection_string = connection_string
        self.nc = nc
        self.loop = loop
        # loop.set_debug(True)
        self._vehicle_id = vehicle_id
        self._logger = logging.Logger('NATS')
        self._logger.addHandler(logger_handler)
        self._warnings_handler = warnings_handler

    @asyncio.coroutine
    def on_message(self, msg):
        self._logger.debug("[Received on '{}']: {}".format(
            msg.subject, msg.data.decode()))
        task = self.loop.create_task(
            self._warnings_handler.parse_and_display_warning(msg.data.decode()))
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
        self._logger.info("NATS connected")
        if self._warnings_handler is not None:
            try:
                self.sid = yield from nc.subscribe("vehicle." + self._vehicle_id + ".warning", cb=self.on_message)
                self.sid_demo = yield from nc.subscribe("vehicle." + self._vehicle_id + "-demo.warning", cb=self.on_message)

            except ErrConnectionClosed:
                print("Connection closed prematurely")

        if nc.last_error is not None:
            print("Last Error: {}".format(nc.last_error))

        if nc.is_closed:
            print("Disconnected.")

        self._logger.debug("NATS subscription started")

        yield from nc.publish("vehicle." +
                              self._vehicle_id + ".status", b'Online!')

    def send_message(self, message):
        """Sends a position report to NATS"""
        asyncio.ensure_future(self.nc.publish("vehicle." + self._vehicle_id +
                                              ".position", bytes(message.as_json, "utf-8")))

    @asyncio.coroutine
    def async_close(self):
        self.loop.stop()
        self.loop.close()
        self.nc.close()

    def close(self):
        for task in asyncio.Task.all_tasks():
            task.cancel()
        asyncio.ensure_future(self.async_close())
