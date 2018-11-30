import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout, ErrNoServers
import json
from dencity_bike.model.position import Position
import sys
import datetime

def run(loop):
  nc = NATS()
  nats_connection_string = "nats://username:password@bike.dowhile.se:4222"

  position_bus = {}
  position_bus["lat"] = 57.709548
  position_bus["lon"] = 11.941056
  position_bus["speed"] = 12.5
  position_bus["course"]  = 45
  position_bus["time"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
  position_bus["vehicle_type"] = "bus"

  position_bike = {}
  position_bike["lat"] = 57.709627
  position_bike["lon"] = 11.942357
  position_bike["speed"] = 14.5
  position_bike["course"]  = 330
  position_bike["time"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
  position_bike["vehicle_type"] = "bicycle"


  try:
    yield from nc.connect(io_loop=loop, servers=[nats_connection_string])
  except ErrNoServers as e:
    print(e)
    return

  @asyncio.coroutine
  def message_sender(position, vehicle_id):
    subject = "vehicle." + vehicle_id + ".position"
    yield from nc.publish(subject, json.dumps(position).encode())


  @asyncio.coroutine
  def message_printer(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print("Received a message on '{subject} {reply}': {data}".format(
      subject=subject, reply=reply, data=data))
    sys.stdout.flush()

  yield from nc.subscribe("*.>", cb=message_printer)
  yield from message_sender(position_bus, "testBUS1")
  yield from message_sender(position_bike, "testBIKE1")
  

  try:
    # Flush connection to server, returns when all messages have been processed.
    # It raises a timeout if roundtrip takes longer than 1 second.
    yield from nc.flush(1)
  except ErrTimeout:
    print("Flush timeout")

  yield from asyncio.sleep(1, loop=loop)
  yield from nc.close()

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(run(loop))
  loop.close()
