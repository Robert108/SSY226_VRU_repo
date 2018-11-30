import React from 'react';
import { Polygon } from 'react-leaflet';
// import MapUtils from '../../../utils/map.utils';

const busDetectionPolygon = props => {
  /*
  let coordFrom = props.coordFrom;
  const origin = GeometryUtil.destination(coordFrom, 0, 0);
  const pointA = GeometryUtil.destination(origin, -45, 2);
  const pointB = GeometryUtil.destination(pointA, 0, 4);
  const pointC = GeometryUtil.destination(pointB, 90, 2.8);
  const pointD = GeometryUtil.destination(pointC, 180, 4);
  const pointE = GeometryUtil.destination(pointD, 225, 2);
  */

  let polygonPoints = props.polyDefinition;

  /*polygonPoints = polygonPoints.map(polygonPoint => {
    return [polygonPoint.lat, polygonPoint.lon];
  });

  polygonPoints = MapUtils.rotatePoints(
    [coordFrom.lat, coordFrom.lon],
    polygonPoints,
    props.heading
  );*/

  /*if (props.map) {
    polygonPoints = polygonPoints.map(point => {
      return GeometryUtil.rotatePoint(
        props.map,
        point,
        props.heading,
        coordFrom
      );
    });
  }*/

  return <Polygon positions={polygonPoints} color={props.color} />;
};

export default busDetectionPolygon;
