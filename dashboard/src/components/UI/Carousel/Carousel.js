import React from 'react';
import { React_Bootstrap_Carousel } from 'react-bootstrap-carousel';
import './Carousel.css';

class Carousel extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      autoplay: false
    };
  }
  onSelect = (active, direction) => {
    console.log(`active=${active} && direction=${direction}`);
  };
  slideNext = () => {
    this.slider.slideNext();
  };
  slidePrev = () => {
    this.slider.slidePrev();
  };
  goToSlide = () => {
    this.slider.goToSlide(4);
  };
  autoplay = () => {
    this.setState({ autoplay: !this.state.autoplay });
  };
  _changeIcon = () => {
    let { leftIcon, rightIcon } = this.state;
    if (leftIcon && rightIcon) {
      this.setState({
        leftIcon: undefined,
        rightIcon: undefined
      });
    } else {
      this.setState({
        leftIcon: <span className="glyphicon glyphicon-glass" />,
        rightIcon: <span className="glyphicon glyphicon-music" />
      });
    }
  };
  render() {
    let { leftIcon, rightIcon } = this.state;

    return (
      <React_Bootstrap_Carousel
        animation={true}
        autoplay={this.state.autoplay}
        slideshowSpeed={7000}
        defaultActiveIndex={0}
        leftIcon={leftIcon}
        rightIcon={rightIcon}
        onSelect={this.onSelect}
        ref={r => (this.slider = r)}
      >
        {this.props.children}
      </React_Bootstrap_Carousel>
    );
  }
}

export default Carousel;
