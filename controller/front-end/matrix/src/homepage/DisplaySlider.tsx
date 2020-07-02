import React from 'react';
import { Slider, Typography, Switch, FormControlLabel } from '@material-ui/core';
import { Container, Row, Col, Button,
         Form, FormGroup, Label, Input } from 'reactstrap';


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
    this.processIntAttribute = this.processIntAttribute.bind(this);
    this.processStrAttribute = this.processStrAttribute.bind(this);
    this.processBoolAttribute = this.processBoolAttribute.bind(this);
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
    }).then(() => {window.location.reload()} )
    
  }

  processIntAttribute(key : string) {
    const { ledAttrs } = this.state;
    return ( 
      <Col xs="8" md={{size : 4, offset: 4}}  id={key}>
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
      </Col>  
    );
  } 
  
  processStrAttribute(key : string) {
    return (
      <FormGroup> 
        <Label> {key} </Label>
        <Input 
          id={key} 
          name={key} 
          onChange={(event : any) => {
            var curLed = this.state.ledAttrs;
            curLed[key]["value"] = event.target.value;
            this.setState({ledAttrs : curLed})
          }}
          placeholder="Type here..."/>
      </FormGroup> 
    );
  }

  processBoolAttribute(key : string) {
    const { ledAttrs } = this.state;
    return (
      <Col xs="8" md={{size : 4, offset: 4}}  id={key}>
        <FormControlLabel label={key} control={
          <Switch
            checked={ledAttrs[key]["value"]}
            onChange={(event : any) => {
              var curLed = this.state.ledAttrs;
              curLed[key]["value"] = event.target.checked;
              this.setState({ledAttrs : curLed})
            }}
           />}
         />
      </Col>
    );
  }
 
  render() {
    const { loaded, ledAttrs } = this.state;
    var sliderIntArr : any[] = [];
    var sliderStrArr : any[] = [];
    var sliderBoolArr : any[] = [];
    if (loaded) {
      for (let key in ledAttrs) {
        if (ledAttrs[key]["type"] === 'int') {
          sliderIntArr.push(this.processIntAttribute(key));
        } else if (ledAttrs[key]["type"] === 'str') {
          sliderStrArr.push(this.processStrAttribute(key));
        } else if (ledAttrs[key]["type"] === 'bool') {
          sliderBoolArr.push(this.processBoolAttribute(key));
        }
      }
    }

    return (
      <Container fluid>
        <Row>
          {sliderBoolArr}
        </Row>
        <Row xs="8" md="6"> 
          {sliderIntArr} 
        </Row>
        <Row>
          <Col xs="12" md="8" lg={{size : 6, offset : 3}}>
            <Form> 
              {sliderStrArr} 
            </Form>
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
