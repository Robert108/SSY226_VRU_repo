import React, { Component } from 'react';
import CollisionDetectionMap from './components/CollisionDetectionMap/CollisionDetectionMap';
import CrashReport from './components/CrashReport/CrashReport';
import Header from './components/UI/Header/Header';
import AppConstants from './constants/AppConstants';
import ParseUtils from './utils/parse.utils';
import { latLng } from 'leaflet';
import Aux from './hoc/AuxilaryComponent/AuxilaryComponent';
import logo from './assets/images/elogo.png';
import Modal from './components/UI/Modal/Modal';
import Loader from './components/UI/Loader/Loader';
import Carousel from './components/UI/Carousel/Carousel';
import './App.css';
import DataUtils from './utils/data.utils';
var nats = require('websocket-nats');

class App extends Component {
  // Complete State of Application
  state = {
    buses: [],
    bikes: [],
    warnings: []
  };

  // Nat connection ids
  natSChannels = [];

  // Nat Connection
  natConn = null;

  // Collection detection View, close timer
  warningMessageTimeout = null;

  componentDidMount() {
    // If development user the variable in .env.developlment.local file, else use hosting ip
    const HOST =
      process.env.NODE_ENV === 'development'
        ? process.env.REACT_APP_HOST
        : window.location.host;

    // Create Nat connection
    this.natConn = nats.connect({
      url: `wss://${HOST}/nats`,
      user: 'monitor',
      pass: 'monitor'
    });

    // Nat postion channel
    const natPositionSID = this.natConn.subscribe(
      AppConstants.nat.subscriptions.positions,
      (msg, reply, topic) => {
        // console.log('=========================================');
        // console.log('Topic:', topic);
        // console.log('Message:', msg);
        // console.log('=========================================');

        const messageJson = JSON.parse(msg);

        // If Vehicle message, begin parsing logic to update the buses and bikes array
        this.setState(state => {
          const parsedResponse = ParseUtils.normalizeVehicleResponse(
            topic,
            messageJson
          );

          // Find out which array to insert data
          let vehicleArray = null;
          if (ParseUtils.isBusMessage(messageJson)) {
            vehicleArray = state.buses;
          } else {
            vehicleArray = state.bikes;
          }

          // If vehicle is not present in array then create it
          vehicleArray = DataUtils.getUpdatedVehicleArray(
            vehicleArray,
            parsedResponse
          );

          // Update state
          if (ParseUtils.isBusMessage(messageJson)) {
            return {
              ...state,
              buses: vehicleArray
            };
          } else {
            return {
              ...state,
              bikes: vehicleArray
            };
          }
        });
      }
    );

    this.natSChannels.push(natPositionSID);

    // Nat Warning Channel
    const natWarningSID = this.natConn.subscribe(
      AppConstants.nat.subscriptions.warnings,
      (msg, reply, topic) => {
        // console.error('=========================================');
        // console.error('Topic:', topic);
        // console.error('Message:', msg);
        // console.error('=========================================');

        try {
          this.setState(prevState => {
            const messageJson = JSON.parse(msg);
            let newState = [];

            const parsedResponse = ParseUtils.normalizeWarningResponse(
              topic,
              messageJson
            );

            const oldState = DataUtils.getExistingObject(
              prevState.warnings.slice(0),
              parsedResponse.id
            );

            if (oldState && oldState.warningMessageTimeout)
              clearTimeout(oldState.warningMessageTimeout);

            this.setNewTimeout(
              parsedResponse,
              this.setNewTimeoutCallback(parsedResponse),
              2000
            );

            newState = DataUtils.getUpdatedWarningArray(
              prevState.warnings.slice(0),
              parsedResponse
            );

            return {
              ...prevState,
              warnings: newState
            };
          });
        } catch (error) {
          // log any errors
          console.error(error);

          // clean up
          this.disconnectNats(natWarningSID);
        }
      }
    );

    this.natSChannels.push(natWarningSID);
  }

  setNewTimeout = (warning, callback, delay) => {
    const id = setTimeout(function() {
      callback();
    }, delay);
    warning['warningMessageTimeout'] = id;
  };

  setNewTimeoutCallback = warning => {
    return () => {
      this.setState((prevState, props) => {
        const updatedArray = DataUtils.removeElementForArray(
          prevState.warnings,
          warning.id
        );

        return {
          ...prevState,
          warnings: updatedArray
        };
      });
    };
  };

  componentWillUnmount() {
    // clean up
    this.disconnectAllNatChannels();
  }

  disconnectNats(natSID) {
    this.natConn.unsubscribe(natSID);
  }

  disconnectAllNatChannels() {
    this.natSChannels.forEach(natSChannelId => {
      this.disconnectNats(natSChannelId);
    });
  }

  render() {
    const loader = this.state.warnings.length === 0 ? <Loader /> : null;

    const crashDetectionView = () => {
      const views = this.state.warnings.map(warning => {
        return (
          <CrashReport
            key={warning.id}
            center={warning.center}
            bus={warning.bus}
            bike={warning.bike}
            proximity={warning.threat_distance}
          />
        );
      });

      if (views.length === 1) return views[0];

      return <Carousel>{views}</Carousel>;
    };

    return (
      <Aux>
        <Modal show={this.state.warnings.length > 0}>
          {loader}
          {crashDetectionView()}
        </Modal>
        <div className="App_Header">
          <Header
            title="ElectriCity"
            image={logo}
            sideTitle="Traffic Dashboard - Connected Bike"
          />
        </div>
        <div className="App_Map">
          <CollisionDetectionMap
            showLegend={this.state.warnings.length === 0}
            showPolygons={false}
            buses={this.state.buses}
            bikes={this.state.bikes}
            zoom={AppConstants.map.starting.zoom}
            center={latLng(...AppConstants.map.starting.position)}
          />
        </div>
      </Aux>
    );
  }
}

export default App;
