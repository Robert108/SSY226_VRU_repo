import React, { PureComponent } from 'react';
import { Marker } from 'react-leaflet';
import AppConstants from '../../../constants/AppConstants';
import MapUtils from './../../../utils/map.utils';

class BusMarker extends PureComponent {
  state = {
    heading: null,
    vehicleType: AppConstants.icons.getBus(),
    lat: null,
    lng: null
  };

  componentDidUpdate() {
    this.setState({
      ...this.state,
      lat: this.props.position.lat,
      lon: this.props.position.lon,
      heading: this.props.heading
    });
  }

  render() {
    const icon = MapUtils.getMarkerIcon(
      'bus-marker',
      [40, 40, false],
      this.state.vehicleType,
      this.props.heading == null ? this.state.heading : this.props.heading
    );

    return <Marker position={this.props.position} icon={icon} />;
  }
}

export default BusMarker;
