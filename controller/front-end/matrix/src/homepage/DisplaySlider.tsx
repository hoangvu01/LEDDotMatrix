import React from 'react';
import Slider from '@material-ui/core/Slider';

class DisplaySlider extends React.Component {
  constructor(props : any) {
    super(props);
    this.state = {
      loaded: true
    }
    
  }


  render() {
    return (
      <Slider 
        defaultValue={50}
        min={0}
        max={100}
        step={10}
      />
    );
  }
}

export default DisplaySlider;
