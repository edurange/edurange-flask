import "./scenario_options.css";
import React, { useState, useEffect } from 'react';
import Container from 'react-bootstrap/Container'; 
import Row from 'react-bootstrap/Row'; 
import Col from 'react-bootstrap/Col'; 
import Button from 'react-bootstrap/Button'

export default function scenario_options() {
     const [selectedScenario, setSelectedScenario] = useState("");
     const setScenario = (e) => {setSelectedScenario("Metasploitable")};   
     const scenario_dict = [{Difficulty:"e", Scenario:"Getting Started"}, {Difficulty:"e", Scenario:"File Wrangler"},
     {Difficulty:"m", Scenario:"Elf Infection"}, {Difficulty:"m", Scenario:"Strace"}, {Difficulty:"m", Scenario:"Treasure Hunt"},
     {Difficulty:"m", Scenario:"SSH Inception"}, {Difficulty:"m", Scenario:"Total Recon"}, {Difficulty:"m", Scenario:"Webfu"},
     {Difficulty:"h", Scenario:"Metasploitable"}];

  return (
    <div> 
     <h1>Choose Scenario</h1>
     <h1>{selectedScenario}</h1>
     <Container> 
      <h3></h3>
       <Row className="easyScenarioButtons"> 
            <Col><Button onClick={setScenario} className="e">Getting Started</Button></Col>
            <Col><Button onClick={setScenario} className="e">File Wrangler</Button></Col>
            <Col></Col>
       </Row>
       <h3></h3>
       <Row className="mediumScenarioButtons">
            <Col><Button onClick={setScenario} className="m">Elf Infection</Button></Col>
            <Col><Button onClick={setScenario} className="m">Strace</Button></Col>
            <Col><Button onClick={setScenario} className="m">Treasure Hunt</Button></Col>
       </Row>
       <h3></h3>
       <Row className="mediumScenarioButtons">
            <Col><Button onClick={setScenario} className="m">SSH Inception</Button></Col>
            <Col><Button onClick={setScenario} className="m">Total Recon</Button></Col>
            <Col><Button onClick={setScenario} className="m">Webfu</Button></Col>
       </Row>
       <h3></h3>
       <Row className="hardScenarioButtons">
            <Col><Button onClick={setScenario} className="h">Metasploitable</Button></Col>
            <Col></Col>
            <Col></Col>
      </Row>
     </Container>     
    </div>
  )
}
