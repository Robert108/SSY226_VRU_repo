import React from 'react';
import Aux from '../../hoc/AuxilaryComponent/AuxilaryComponent';
import CollisionDetectionMap from '../CollisionDetectionMap/CollisionDetectionMap';
import Header from './../UI/Header/Header';
import './CrashReport.css';

const crashReport = props => {
  const threatDistance = `Distance Proximity: ${parseFloat(
    props.proximity
  ).toFixed(2)} meters`;

  const report = (
    <Aux>
      <div className="CrashReport">
        <div className="CrashReport__Header">
          <Header title="Vehicles Approaching" sideTitle={threatDistance} />
        </div>
        <div className="CrashReport__Body">
          <CollisionDetectionMap
            showLegend={true}
            showPolygons={true}
            center={props.center}
            buses={[props.bus]}
            bikes={[props.bike]}
            zoom={20}
          />
        </div>
      </div>
    </Aux>
  );

  return report;
};

export default crashReport;
