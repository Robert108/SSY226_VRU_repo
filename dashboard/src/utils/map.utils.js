import Leaflet from 'leaflet';

export default (() => {
  // return html of marker with correct bearing
  function _getMarkerWithBearing(vehicleType, bearing) {
    let vehicle = vehicleType.replace(
      '{svg-transform}',
      'rotate(' + (bearing == null ? 0 : bearing) + ')'
    );
    return vehicle;
  }

  function _getDistance(lat1, lon1, lat2, lon2) {
    var R = 6371000; // meter
    var Phi1 = _toRad(lat1);
    var Phi2 = _toRad(lat2);
    var DeltaPhi = _toRad(lat2 - lat1);
    var DeltaLambda = _toRad(lon2 - lon1);

    var a =
      Math.sin(DeltaPhi / 2) * Math.sin(DeltaPhi / 2) +
      Math.cos(Phi1) *
        Math.cos(Phi2) *
        Math.sin(DeltaLambda / 2) *
        Math.sin(DeltaLambda / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var d = R * c;

    return d;
  }

  function _toRad(val) {
    return (val * Math.PI) / 180;
  }

  return {
    getMarkerIcon: (className, iconSize, markerType, bearing) => {
      return Leaflet.divIcon({
        className,
        iconSize,
        html: _getMarkerWithBearing(markerType, bearing)
      });
    },

    areCoordinatesDistantEnough(coord_one, coord_two) {
      return (
        JSON.stringify(coord_one.lat.toString().substring(8, 3)) !==
        JSON.stringify(coord_two.lat.toString().substring(8, 3))
      );
    },

    getBearing: (coordFrom, coordTo, currentBearing) => {
      // Can also use GeometryUtil from Leaflet
      let d = _getDistance(
        coordFrom.lat,
        coordFrom.lon,
        coordTo.lat,
        coordTo.lon
      );

      if (d < 0.5) {
        return currentBearing;
      }
      return (
        (Math.atan2(coordTo.lon - coordFrom.lon, coordTo.lat - coordFrom.lat) *
          180) /
        Math.PI
      );
    },

    rotatePoints: function(center, points, yaw) {
      if (yaw === undefined) return points;
      var res = [];
      var angle = yaw * (Math.PI / 180); // not really sure what this is
      for (var i = 0; i < points.length; i++) {
        var p = points[i];
        // translate to center
        var p2 = [p[0] - center[0], p[1] - center[1]];
        // rotate using matrix rotation
        var p3 = [
          Math.cos(angle) * p2[0] - Math.sin(angle) * p2[1],
          Math.sin(angle) * p2[0] + Math.cos(angle) * p2[1]
        ];
        // translate back to center
        var p4 = [p3[0] + center[0], p3[1] + center[1]];
        // done with that point
        res.push(p4);
      }
      return res;
    }
  };
})();
