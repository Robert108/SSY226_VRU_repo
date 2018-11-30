export default {
  nat: {
    subscriptions: {
      positions: 'vehicle.*.position',
      warnings: 'collision_avoidance.warning'
    }
  },
  vehicleType: {
    bus: 'bus',
    bike: 'bicycle'
  },
  map: {
    starting: {
      position: [57.7051292, 11.9466446],
      zoom: 13
    }
  },
  icons: {
    getBus: isRaw =>
      '<svg ' +
      (isRaw ? '' : 'transform="{svg-transform}"') +
      ' width="20px" height="20px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="448.199px" height="448.199px" viewBox="0 0 448.199 448.199" style="enable-background:new 0 0 448.199 448.199;" xml:space="preserve"> <g> <polygon fill="blue" points="224.1,0 30.256,448.199 224.1,350.775 417.943,448.199 	"/> </g> <g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg>',
    getBike: isRaw =>
      '<svg ' +
      (isRaw ? '' : 'transform="{svg-transform}"') +
      ' width="20px" height="20px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="448.199px" height="448.199px" viewBox="0 0 448.199 448.199" style="enable-background:new 0 0 448.199 448.199;" xml:space="preserve"> <g> <polygon fill="green" points="224.1,0 30.256,448.199 224.1,350.775 417.943,448.199 	"/> </g></svg>'
  }
};
