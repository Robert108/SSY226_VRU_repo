import React from 'react';
import './Backdrop.css';

const backdrop = props => (props.show ? <div className="Backdrop" /> : null);

export default backdrop;
