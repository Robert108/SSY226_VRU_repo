# PEWCAS APIs

## Overview

### Bike <-> PEWCAS

The communication between a bike and the backend system is via NATS messaging, where the backend receives positioning data from the bike and sends collison avoidance messages when a potential collision has been detected

The positioning object is modeled after the data provided by the `gpsd` solution http://www.catb.org/gpsd/ to minimize the complexity of the code running on the bike side.

##### Position message

The Position message data is a JSON object with the following members

`vehicle_type` _(mandatory)_ String. Type of vehicle. Must be `bicycle` for bikes. \
`client_version` _(mandatory)_ Number. The version of the hardware/software running on the bicycle \

Position data: (See http://www.catb.org/gpsd/gpsd_json.html for details)
`time` _(mandatory)_ ISO8601 timestamp. The time of the position measurement. \
`ept` _(optional)_ Number. Estimated time error in seconds. \
`lat` _(mandatory)_ Number. Latitude in degrees. (+/- signifies north/south) \
`lon` _(mandatory)_ Number. Longitude in degrees. (+/- signifies east/west) \
`alt` _(optional)_ Number. Altitude in meters. \
`epx` _(optional)_ Number. Longitude error in meters. \
`epy` _(optional)_ Number. Latitude error in meters. \
`epv` _(optional)_ Number. Altitude error in meters. \
`course` _(optional)_ Number. Course over ground, degrees from true north. \
`speed` _(optional)_ Number. Speed in meters per second. \
`climb` _(optional)_ Number. Climb rate in meters per second. (+/- signifies ascent/descent) \
`eps` _(optional)_ Number. Speed error in meters per second.

Example body:

```json
{
    "vehicle_type": "bicycle",
    "client_version": 1,
    "time": "2005-06-08T10:34:48.283Z",
    "ept": 0.005,
    "lat": 46.498293369,
    "lon": 7.567411672,
    "alt": 1343.127,
    "course": 10.3788,
    "speed": 4.091,
    "climb": -0.085
}

```

##### Response

HTTP Status: 200 \
Content type: `application/json`

The response body is a JSON object with the following content

`status` _(mandatory)_ Enum (`ok`, `warning`). Signifies wheter a collision warning is to be presented \
`warnings` _(optional)_ Array: Warning. A list of warning objects to notify the rider about.

Warning object:

`type` _(mandatory)_ Enum (`collision`). Type of warning. \
`threat_identifier` _(optional)_ Enum (`bus`). An identifier for the threat cause.
`threat_direction` _(mandatory)_ Number. Direction of threat, degrees from current heading. \
`threat_distance` _(optional)_ Number. Distance to threat in meters. \
`priority` _(optional)_ Enum (`high`, `medium`, `low`). The priority/urgency of the warning.

Example body:

```json
{
    "status": "warning",
    "warnings": [
        {
            "type": "collision",
            "threat_identifier": "bus",
            "threat_direction": 194.2,
            "threat_distance": 24.6,
            "priority": "high"
        }
    ]
}
```