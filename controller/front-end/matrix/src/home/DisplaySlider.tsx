import React from 'react';
import { Slider } from '@materials-ui/core';

export default class DisplaySlider extends React.Component{
 
  constructor(props) {
    super(props);
  }

  render() {
    return(
      <Slider
        defaultValue={0}
        getAriaValueText={valuetext}
        marks={true}
        step={1}
        min={0}
        max={10}
      />
    )
  };

}

