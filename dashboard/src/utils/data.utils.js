export default (() => {
  return {
    getUpdatedWarningArray: (warningArray, parsedResponse) => {
      let warning =
        warningArray.filter(vehicle => vehicle.id === parsedResponse.id)
          .length > 0;
      if (!warning) {
        warningArray.push({
          ...parsedResponse
        });
      } else {
        // If vehicle present in array find it and update the postions arrays
        warningArray = warningArray.map(warning => {
          if (warning.id === parsedResponse.id) {
            warning = { ...warning, ...parsedResponse };
          }

          return warning;
        });
      }
      return warningArray;
    },
    getExistingObject: (warnings, id) => {
      const oldState = warnings.filter(warning => {
        return warning.id === id;
      });

      if (oldState.length > 0) {
        return oldState[0];
      } else {
        return null;
      }
    },
    removeElementForArray: (objArray, id) => {
      let indexNoOfItem = null;

      objArray.forEach((obj, index) => {
        if (obj.id === id) indexNoOfItem = index;
      });

      console.log(`Index to be removed ${indexNoOfItem}`);

      indexNoOfItem !== null && objArray.splice(indexNoOfItem, 1);

      return objArray;
    },
    updateArray: (array, obj) => {
      const updatedArray = array.map(elem => {
        if (elem.id === obj.id) {
          elem = obj;
        }

        return elem;
      });
      return updatedArray;
    },
    getUpdatedVehicleArray: (vehicleArray, parsedResponse) => {
      let vehicle =
        vehicleArray.filter(vehicle => vehicle.id === parsedResponse.id)
          .length > 0;
      if (!vehicle) {
        vehicleArray.push({
          id: parsedResponse.id,
          type: parsedResponse.type,
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
