import React, { Component } from 'react';
import leaflet, { latLng } from 'leaflet';
import { Map, TileLayer } from 'react-leaflet';
import Aux from './../../hoc/AuxilaryComponent/AuxilaryComponent';
import BusMarker from './../Markers/BusMarker/BusMarker';
import BikeMarker from './../Markers/BikeMarker/BikeMarker';
import BusDetectionPolygon from './../Polygons/BusDetection/BusDetection';
import BikeDetectionPolygon from './../Polygons/BikeDetection/BikeDetection';
import AppConstants from '../../constants/AppConstants';
import bus from './../../assets/images/bus.png';
import bike from './../../assets/images/bike.png';
import './CollisionDetectionMap.css';

class CollisionDetectionMap extends Component {
  componentDidMount() {
    // this.addLegend();
  }

  componentDidUpdate() {
    // if (!this.props.showLegend) {
    //   this.map.leafletElement.removeControl(this.legendControl);
    // } else {
    //   this.legendControl.addTo(this.map.leafletElement);
    // }
  }

  addLegend() {
    this.legendControl = leaflet.control();

    this.legendControl.onAdd = function(map) {
      this.mapLegend = leaflet.DomUtil.create('div', 'Legend');
      this.update();
      return this.mapLegend;
    };

    this.legendControl.update = function(props) {
      this.mapLegend.innerHTML =
        '<div class="Legend__Container">' +
        '<div class="Legend__Container-Row">' +
        AppConstants.icons.getBus(true) +
        ' <span><img style="width: 30px" src="' +
        bus +
        '"/></span></div>' +
        '<div class="Legend__Container-Row">' +
        AppConstants.icons.getBike(true) +
        ' <span><img  style="width: 30px" src="' +
        bike +
        '"/></span></div>' +
        '</div>';
    };

    this.legendControl.addTo(this.map.leafletElement);
  }

  render() {
    const tileLayer = (
      <TileLayer
        attribution="&amp;copy <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
    );

    const getBusDetectionPolygon = bus =>
      this.props.showPolygons ? (
        <BusDetectionPolygon
          polyDefinition={bus.projected_position}
          coordFrom={latLng([bus.lat, bus.lon])}
          heading={bus.heading}
          color="blue"
        />
      ) : null;

    const busLayer = this.props.buses.map(bus => {
      return (
        <Aux key={bus.id}>
          {getBusDetectionPolygon(bus)}
          <BusMarker
            position={latLng([bus.lat, bus.lon])}
            heading={bus.heading}
          />
        </Aux>
      );
    });

    const getBikeDetectionPolygon = bike =>
      this.props.showPolygons ? (
        <BikeDetectionPolygon
          polyDefinition={bike.projected_position}
          coordFrom={latLng([bike.lat, bike.lon])}
          heading={bike.heading}
          // color="green"
          color="blue" // Use same color for everything
        />
      ) : null;

    const bikeLayer = this.props.bikes.map(bike => {
      return (
        <Aux key={bike.id}>
          {getBikeDetectionPolygon(bike)}
          <BikeMarker
            position={latLng([bike.lat, bike.lon])}
            heading={bike.heading}
          />
        </Aux>
      );
    });

    return (
      <Map
        ref={c => (this.map = c)}
        center={this.props.center}
        zoom={this.props.zoom}
        maxZoom={18}
      >
        {tileLayer}
        {busLayer}
        {bikeLayer}
      </Map>
    );
  }
}

export default CollisionDetectionMap;
