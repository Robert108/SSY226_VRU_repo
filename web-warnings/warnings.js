var nats = null;
var sid = null;
var lastTimeout = null;
var TIMEOUT = 5000;

function handleInput() {
  var id = document.getElementById('input').value;
  window.location.hash = id;
  // checkFragment() will be triggered here
}

function checkFragment() {
  var id = window.location.hash.substr(1);
  if (id) {
    printID(id);
    hideInput();
    subscribe(id);
  } else {
    unsubscribe();
    printID('');
    showInput();
  }
}

function connectNATS() {
  if (nats) nats.close();

  nats = NATS.connect({
    url: 'wss://' + window.location.host + '/nats',
    user: 'monitor',
    pass: 'monitor',
    maxReconnectAttempts: -1
  });

  nats.on('connect', function() {
    printConnected();
  });
  nats.on('reconnect', function() {
    printConnected();
  });
  nats.on('disconnect', function() {
    printDisconnected();
  });
}

function subscribe(id) {
  if (!nats) connectNATS();
  if (sid) nats.unsubscribe(sid);
  var subject = 'vehicle.' + id + '.warning';
  sid = nats.subscribe(subject, handleWarning);
}

function unsubscribe() {
  if (nats && sid) nats.unsubscribe(sid);
}

function handleWarning(message, reply, subject) {
  console.log(subject, message);
  var warning = JSON.parse(message);

  var rotation = 'rotateZ(0deg)';
  if ('threat_direction' in warning) {
    rotation = 'rotateZ(' + Math.round(warning.threat_direction) + 'deg)';
  }
  var directionElement = document.getElementById('direction');
  directionElement.style['-webkit-transform'] = rotation;
  directionElement.style['-moz-transform'] = rotation;
  directionElement.style['-ms-transform'] = rotation;
  directionElement.style['-o-transform'] = rotation;
  directionElement.style['transform'] = rotation;

  if ('threat_distance' in warning) {
    var distance = Math.round(warning.threat_distance);
    document.getElementById('distance').innerHTML = distance + ' m';
  } else {
    document.getElementById('distance').innerHTML = '';
  }

  var threatImage = document.getElementById('threat-type');
  threatImage.src = 'img/warning.svg';
  if ('threat_identifier' in warning) {
    var threat = warning.threat_identifier;

    // Here we should look at the actual vehicle type instead of ID name
    if (threat.indexOf('bicycle') !== -1) {
      threatImage.src = 'img/bike.svg';
    } else if (threat.indexOf('bike') !== -1) {
      threatImage.src = 'img/bike.svg';
    } else if (threat.indexOf('bus') !== -1) {
      threatImage.src = 'img/bus.svg';
    } else if (threat.indexOf('car') !== -1) {
      threatImage.src = 'img/car.svg';
    } else if (threat.indexOf('person') !== -1) {
      threatImage.src = 'img/pedestrian.svg';
    } else if (threat.indexOf('smv') !== -1) {
      threatImage.src = 'img/excavator.svg';
    }
  }
  showWarning();

  if (lastTimeout) window.clearTimeout(lastTimeout);
  lastTimeout = setTimeout(hideWarning, TIMEOUT);
};

function showInput() {
  document.getElementById('subscribe').style.display = 'block';
  document.getElementById('warning').style.display = 'none';
  document.getElementsByTagName('footer')[0].style.display = 'none';
};

function hideInput() {
  document.getElementById('subscribe').style.display = 'none';
  document.getElementsByTagName('footer')[0].style.display = 'block';
};

function showWarning() {
  document.body.style.backgroundColor = '#c00000';
  document.getElementById('subscribe').style.display = 'none';
  document.getElementById('warning').style.display = 'block';
  document.getElementsByTagName('footer')[0].style.display = 'none';
};

function hideWarning() {
  document.body.style.backgroundColor = '#000';
  document.getElementById('subscribe').style.display = 'none';
  document.getElementById('warning').style.display = 'none';
  document.getElementsByTagName('footer')[0].style.display = 'block';
};

function printConnected() {
  document.getElementById('status').innerHTML = 'Connected';
  document.getElementById('status').style.color = '#00c000';
};

function printDisconnected() {
  document.getElementById('status').innerHTML = 'Disconnected';
  document.getElementById('status').style.color = '#c00000';
};

function printID(id) {
  document.getElementById('id').innerHTML = id;
};

function toggleFullscreen() {
  if (document.fullscreenElement || document.mozFullScreenElement ||
      document.webkitFullscreenElement || document.msFullscreenElement) {
    closeFullscreen();
  } else {
    openFullscreen();
  }
}

function openFullscreen() {
  var element = document.documentElement;
  if (element.requestFullscreen) {
    element.requestFullscreen();
  } else if (element.mozRequestFullScreen) {
    element.mozRequestFullScreen();
  } else if (element.webkitRequestFullscreen) {
    element.webkitRequestFullscreen();
  } else if (element.msRequestFullscreen) {
    element.msRequestFullscreen();
  }
}

function closeFullscreen() {
  if (document.exitFullscreen) {
    document.exitFullscreen();
  } else if (document.mozCancelFullScreen) {
    document.mozCancelFullScreen();
  } else if (document.webkitExitFullscreen) {
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) {
    document.msExitFullscreen();
  }
}

window.onhashchange = checkFragment;

// Entry point to the script:
checkFragment();
