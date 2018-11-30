import React from 'react';
import './Loader.css';

const loader = props => {
  return (
    <div className="lds-ring">
      <div />
      <div />
      <div />
      <div />
    </div>
  );
};

export default loader;
