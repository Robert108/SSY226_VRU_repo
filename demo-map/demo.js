var vehicles = {};

var map = new google.maps.Map(document.getElementById('map'), {
  mapTypeId: google.maps.MapTypeId.ROADMAP,
  center: { lat: 57.7050, lng: 11.9750 },
  zoom: 13,
  maxZoom: 20
});

var hideOverlay = function() {
  document.getElementById('overlay').style.display = 'none';
};

var showOverlay = function() {
  document.getElementById('overlay').style.display = 'block';
};

var fitBounds = function() {
  var bounds = new google.maps.LatLngBounds();
  for (var id in vehicles) {
    if (vehicles[id].marker.getPosition()) {
      bounds.extend(vehicles[id].marker.getPosition());
    }
  }
  if (!bounds.isEmpty()) {
    map.fitBounds(bounds);
  }
};

var newVehicleMarker = function(color, id, type) {
  var icon = {
    path: google.maps.SymbolPath.CIRCLE,
    anchor: new google.maps.Point(0,0),
    rotation: 0,
    strokeWeight: 1,
    strokeColor: '#999',
    fillColor: color,
    fillOpacity: 1,
    scale: 5
  };
  var infoWindow = new google.maps.InfoWindow({
    content: '<code>ID: <b>' + id + '</b><br>' +
      'TYPE: <b>' + type + '</b></code>'
  });
  var marker = new google.maps.Marker({ icon: icon });
  marker.addListener('click', function() {
    infoWindow.open(map, marker);
  });
  return marker;
};

var newPolyline = function(color) {
  var polyline = new google.maps.Polyline({
    strokeColor: color,
    strokeOpacity: 1,
    strokeWeight: 4
  });
  polyline.setMap(map);
  return polyline;
};

var findOrCreateVehicle = function(id, type) {
  if (!(id in vehicles)) {
    var color = '#'+('000000'+(Math.random()*0xFFFFFF<<0).toString(16)).slice(-6);
    vehicles[id] = {
      marker: newVehicleMarker(color, id, type),
      route: newPolyline(color),
      moving: false,
      seen: false
    };
  }
  return vehicles[id];
};

var nats = NATS.connect({
  url: 'wss://' + window.location.host + '/nats',
  user: 'monitor',
  pass: 'monitor'
});

nats.on('connect', function() {
  hideOverlay();
});

nats.on('reconnect', function() {
  hideOverlay();
});

nats.on('disconnect', function() {
  showOverlay();
});

nats.on('error', function(err) {
  console.error(err);
});

nats.subscribe('vehicle.*.position', function(msg, reply, topic) {
  var id = topic.split('.')[1];
  var position = JSON.parse(msg);
  var type = position.vehicle_type;

  var date = new Date();
  var time = date.toTimeString().replace(/ .*/, '');
  var diff = Math.ceil(date.getTime() - (new Date(position.time)).getTime());
  var delay = '(delay '+ Math.ceil(diff) +' ms)';
  console.log(time, id, delay, position);

  var vehicle = findOrCreateVehicle(id, type);
  var point = new google.maps.LatLng(position.lat, position.lon);
  vehicle.marker.setPosition(point);
  vehicle.route.getPath().push(point);

  // Put vehicle on map for the first time
  if (!vehicle.seen) {
    vehicle.marker.setMap(map);
    vehicle.seen = true;
    return;
  }

  // Unknown heading should mean that vehicle is stationary
  if (position.course == null) {
    if (vehicle.moving) {
      // Switch from arrow (moving) to circle (stationary)
      vehicle.marker.icon.path = google.maps.SymbolPath.CIRCLE;
      vehicle.marker.icon.anchor = new google.maps.Point(0,0);
      vehicle.marker.setMap(map);
      vehicle.moving = false;
    }
    return;
  }

  // Skip small heading updates to have less marker redrawing
  if (vehicle.moving &&
      Math.abs(vehicle.marker.icon.rotation - position.course) < 5) {
    return;
  }

  if (!vehicle.moving) {
    // Switch from circle (stationary) to arrow (moving)
    vehicle.marker.icon.path = google.maps.SymbolPath.FORWARD_CLOSED_ARROW;
    vehicle.marker.icon.anchor = new google.maps.Point(0,2);
    vehicle.moving = true;
  }

  vehicle.marker.icon.rotation = position.course;
  vehicle.marker.setMap(map);
});
