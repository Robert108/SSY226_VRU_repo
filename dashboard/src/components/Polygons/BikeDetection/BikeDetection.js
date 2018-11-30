import React from 'react';
import { Polygon } from 'react-leaflet';

const bikeDetectionPolygon = props => {
  let polygonPoints = props.polyDefinition;
  return <Polygon positions={polygonPoints} color={props.color} />;
};

export default bikeDetectionPolygon;
