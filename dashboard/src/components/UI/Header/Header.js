import React from 'react';
import './Header.css';

const header = props => {
  let logoContainer = null;
  if (props.image) {
    logoContainer = (
      <div className="Header_Logo_Container-Logo">
        <img src={props.image} className="Header_Logo-img" alt="company-logo" />
      </div>
    );
  }

  return (
    <div className="Header">
      <div className="Header_Logo_Container">
        {logoContainer}
        <div className="Header_Logo_Container-Title">{props.title}</div>
      </div>
      <div className="Header_Side_Title">{props.sideTitle}</div>
    </div>
  );
};

export default header;
