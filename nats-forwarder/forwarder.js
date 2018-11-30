const mqtt = require('mqtt');
const nats = require('nats');

const MQTT_URL = process.env.MQTT_URL;
const MQTT_USER = process.env.MQTT_USER || '';
const MQTT_PASS = process.env.MQTT_PASS || '';
const MQTT_PREFIX = process.env.MQTT_PREFIX || '';
const MQTT_ID = (process.env.MQTT_ID || 'nats-forwarder-') +
  Math.random().toString(16).substr(2, 8);

const NATS_URL = process.env.NATS_URL;
const NATS_USER = process.env.NATS_USER;
const NATS_PASS = process.env.NATS_PASS;
const NATS_SUBS = process.env.NATS_SUBS.split(',');

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

const mqttConn = mqtt.connect(MQTT_URL, {
  clientId: MQTT_ID,
  username: MQTT_USER,
  password: MQTT_PASS
});

mqttConn.on('connect', () => {
  console.log('Connected to MQTT broker on', MQTT_URL, 'as', MQTT_ID);
});

mqttConn.on('close', () => {
  console.warn('MQTT broker disconnected');
});

mqttConn.on('error', (err) => {
  console.error('MQTT connection error:');
  console.error(err);
  process.exit(1);
});

// FORWARD MESSAGES

for (const subscription of NATS_SUBS) {
  natsConn.subscribe(subscription, (message, reply, subject) => {
    const mqttTopic = MQTT_PREFIX + subject.replace(/\./g, '/');
    mqttConn.publish(mqttTopic, message);
  });
}
