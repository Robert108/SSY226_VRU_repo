const mqtt = require('mqtt');
const nats = require('nats');
const nmea = require('node-nmea');
const vehicles = require('./vehicles.json');

const COORD_MAX_SCALE = 6;
const COURSE_MAX_SCALE = 2;
const SPEED_MAX_SCALE = 2;
const MQTT_TOPIC = '+/vt/service/infohub/gps/nmea0183/rmc';

const MQTT_URL = process.env.MQTT_URL;
const NATS_URL = process.env.NATS_URL;
const NATS_USER = process.env.NATS_USER;
const NATS_PASS = process.env.NATS_PASS;

// NATS CONNECTION

const natsConn = nats.connect({
  url: NATS_URL,
  user: NATS_USER,
  pass: NATS_PASS,
  maxReconnectAttempts: -1 // Retry forever
});

natsConn.on('connect', () => {
  console.log('Connected to NATS server on', NATS_URL);
});

natsConn.on('reconnect', () => {
  console.warn('Reconnected to NATS server');
});

natsConn.on('disconnect', () => {
  console.warn('NATS server disconnected');
});

natsConn.on('close', () => {
  console.error('NATS connection closed');
  process.exit(1);
});

natsConn.on('error', (err) => {
  console.error('NATS connection error:');
  console.error(err);
  process.exit(1);
});

// MQTT CONNECTION

const mqttConn = mqtt.connect(MQTT_URL);

mqttConn.on('connect', () => {
  console.log('Connected to MQTT broker on', MQTT_URL);
  mqttConn.subscribe(MQTT_TOPIC);
});

mqttConn.on('close', () => {
  console.warn('MQTT broker disconnected');
});

mqttConn.on('error', (err) => {
  console.error('MQTT connection error:');
  console.error(err);
  process.exit(1);
});

// POSITION MESSAGES

mqttConn.on('message', (topic, message) => {
  const vin = topic.split('/')[0];
  if (!(vin in vehicles)) {
    console.warn('Unknown vehicle:', vin);
    return;
  }
  const position = parsePosition(message.toString());
  if (position == null) return;

  vehicle = vehicles[vin];
  const id = vehicle.reg_nr;
  position.vehicle_type = vehicle.type;
  natsConn.publish(`vehicle.${id}.position`, JSON.stringify(position));
});

const parsePosition = (gprmc) => {
  const nmeaData = nmea.parse(gprmc);
  if (!nmeaData.valid || !nmeaData.gps) return null;
  const coordinates = nmeaData.loc.geojson.coordinates;
  return {
    time: nmeaData.datetime,
    lat: parseToFixed(coordinates[1], COORD_MAX_SCALE),
    lon: parseToFixed(coordinates[0], COORD_MAX_SCALE),
    course: parseToFixed(nmeaData.track, COURSE_MAX_SCALE, true),
    speed: parseToFixed(knotsToMps(nmeaData.speed.knots), SPEED_MAX_SCALE)
  };
};

// Convert knots to meter per second
const knotsToMps = (knots) => knots * 0.514444;

// Return parsed float with a max number of decimals
const parseToFixed = (num, scale, nullable = false) => {
  const float = parseFloat(parseFloat(num).toFixed(scale));
  if (isNaN(float)) {
    return nullable ? null : 0;
  }
  return float;
};
