# Collision Detector

Program that monitor vehicle positions and send out warnings and intersection information

## Getting Started

Configure the NATS URL in `config.yaml`

```text
docker build -t collision-detector .
docker run collision-detector
```

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Running The Tests

Unittests are located in the test folder.

There are two test utilities:
* `position_monitor.py` - For monitoring all NATS messages.
* `position_publisher.py` - Will publish a pair of vehicles that are on a collision course.

## Message Formats And Subjects

Subject: `collision_avoidance_warning`

```json
{
   "time":"2018-06-11T20:18:01.802462+00:00",
   "threat_distance":77.77905503311386,
   "threat_priority":"medium",
   "bus":{
      "vehicle_id":"testBUS1",
      "position":{
         "vehicle_type":"bicycle",
         "client_version":0,
         "time":"2018-06-11T20:17:54.914125+00:00",
         "lat":57.709548,
         "lon":0.0,
         "speed":12.5,
         "course":45,
         "alt":0.0,
         "climb":0.0,
         "ept":0.0,
         "epv":0.0,
         "epx":0.0,
         "epy":0.0,
         "eps":0.0
      },
      "projected_position":[
         {
            "lat":57.70954649675723,
            "lon":11.941051591675935
         },
         {
            "lat":57.70982753475908,
            "lon":11.941051591675935
         },
         {
            "lat":57.71008446351191,
            "lon":11.941528474910465
         },
         {
            "lat":57.70980342551006,
            "lon":11.942050107113433
         },
         {
            "lat":57.70954649675723,
            "lon":11.941573223878901
         },
         {
            "lat":57.70954649675723,
            "lon":11.941051591675935
         }
      ]
   },
   "bike":{
      "vehicle_id":"testBIKE1",
      "position":{
         "vehicle_type":"bicycle",
         "client_version":0,
         "time":"2018-06-11T20:17:54.915035+00:00",
         "lat":57.709627,
         "lon":0.0,
         "speed":14.5,
         "course":330,
         "alt":0.0,
         "climb":0.0,
         "ept":0.0,
         "epv":0.0,
         "epx":0.0,
         "epy":0.0,
         "eps":0.0
      },
      "projected_position":[
         {
            "lat":57.70962743570176,
            "lon":11.942353585654553
         },
         {
            "lat":57.709711811767,
            "lon":11.941769110355215
         },
         {
            "lat":57.71007683148692,
            "lon":11.94137794980721
         },
         {
            "lat":57.7103073511841,
            "lon":11.942119034791
         },
         {
            "lat":57.70994233146418,
            "lon":11.942510195339008
         },
         {
            "lat":57.70962743570176,
            "lon":11.942353585654553
         }
      ]
   },
   "midpoint":{
      "lat":57.709586966229494,
      "lon":11.941702588665244
   }
}
```

Subject: `vehicle.<id>.warning`

```json
{
   "type":"collision",
   "threat_direction":83.4180553448217,
   "threat_distance":77.77905503311386,
   "threat_priority":"medium",
   "threat_identifier":"testBIKE1"
}
```

Subject: `collision_avoidance_warning`
