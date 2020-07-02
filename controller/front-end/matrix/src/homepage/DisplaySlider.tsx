import React from 'react';
import { Slider, Typography } from '@material-ui/core';
import { Container, Row, Col, Button } from 'reactstrap';


type IState = {
  loaded: boolean,
  ledAttrs: any
}

class DisplaySlider extends React.Component<{}, IState> {
  constructor(props : any) {
    super(props);
    this.state = {
      loaded: false,
      ledAttrs: {}
    };
    this.postLEDAttribute = this.postLEDAttribute.bind(this); 
  }

  componentDidMount() {
    fetch("http://192.168.0.58:5000/api/getDisplay")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({ 
            loaded: true, 
            ledAttrs: result 
          });
        }
      )
  }

  postLEDAttribute() {
    const { ledAttrs } = this.state;
    var ledAttrValues : {[id : string] : string | number} = {}; 
    
    for (let key in ledAttrs) {
      ledAttrValues[key] = ledAttrs[key]["value"];
    }    

    console.log(ledAttrValues);
    fetch('http://192.168.0.58:5000/api/setDisplay', {
      method: 'POST',
      headers: {'Content-Type' : 'Application/json' },
      body: JSON.stringify(ledAttrValues)
    })
  }
 
  render() {
    const { loaded, ledAttrs } = this.state;
    var sliderArr : any[] = [];
    if (loaded) {
      for (let key in ledAttrs) {
        console.log(ledAttrs[key]);
        if (ledAttrs[key]["type"] === 'int') {
          sliderArr.push(
            <div id={key}>
              <Typography id={key}> {key} </Typography>
              <Slider
                defaultValue = {ledAttrs[key]['value'] 
                                ? ledAttrs[key]['value']
                                : ledAttrs[key]['min']}
                step = {1}
                min = {ledAttrs[key]['min']}
                max = {ledAttrs[key]['max']}
                valueLabelDisplay = "auto"
                aria-labelledby = "discrete-slider"
                onChange = { (e, val) => {
                    var curLed = this.state.ledAttrs;
                    curLed[key]["value"] = val;
                    this.setState({ledAttrs : curLed});
                }}
              />   
            </div>  
        
          );
        }
      }
    }

    return (
      <Container>
        <Row> 
          <Col xs="8" md="8" lg="6"> 
            {sliderArr} 
          </Col>
        </Row>
        <Row> 
          <Col> 
            <Button onClick={this.postLEDAttribute}> 
              submit
            </Button>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default DisplaySlider;
