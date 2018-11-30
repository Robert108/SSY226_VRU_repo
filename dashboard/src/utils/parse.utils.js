import AppConstants from '../constants/AppConstants';
import { latLng } from 'leaflet';

export default (() => {
  return {
    isWarningMessage: message => {
      return message['status'] === 'warning';
    },
    isBusMessage: message => {
      return message['vehicle_type'] === AppConstants.vehicleType.bus;
    },
    normalizeVehicleResponse(topic, message) {
      return {
        type: message['vehicle_type'],
        lat: message['lat'],
        lon: message['lon'],
        speed: message['speed'],
        heading: message['course'],
        id: topic.split('.')[1]
      };
    },
    normalizeWarningResponse(topic, message) {
      return {
        ...message,
        id: `${message['bike']['vehicle_id']}-${message['bus']['vehicle_id']}`,
        threat_distance: message['threat_distance'],
        bus: {
          id: message['bus']['vehicle_id'],
          speed: message['bus']['position']['speed'],
          lat: message['bus']['position']['lat'],
          lon: message['bus']['position']['lon'],
          heading: message['bus']['position']['course'],
          projected_position: message['bus']['projected_position'].map(
            latlngObj => {
              return latLng(latlngObj);
            }
          )
        },
        bike: {
          id: message['bike']['vehicle_id'],
          speed: message['bike']['position']['speed'],
          lat: message['bike']['position']['lat'],
          lon: message['bike']['position']['lon'],
          heading: message['bus']['position']['course'],
          projected_position: message['bike']['projected_position'].map(
            latlngObj => {
              return latLng(latlngObj);
            }
          )
        },
        center: latLng(message['midpoint'])
      };
    },
    getUpdatedVehicleArray: (vehicleArray, parsedResponse) => {
      let vehicle =
        vehicleArray.filter(vehicle => vehicle.id === parsedResponse.id)
          .length > 0;
      if (!vehicle) {
        vehicleArray.push({
          id: parsedResponse.id,
          lat: parsedResponse.lat,
          lon: parsedResponse.lon,
          heading: parsedResponse.course,
          speed: parsedResponse.speed
        });
      } else {
        // If vehicle present in array find it and update the postions arrays
        vehicleArray = vehicleArray.map(vehicle => {
          if (vehicle.id === parsedResponse.id) {
            vehicle.lat = parsedResponse.lat;
            vehicle.lon = parsedResponse.lon;
            vehicle.heading = parsedResponse.heading;
            vehicle.speed = parsedResponse.speed;
          }
          return vehicle;
        });
      }
      return vehicleArray;
    }
  };
})();
