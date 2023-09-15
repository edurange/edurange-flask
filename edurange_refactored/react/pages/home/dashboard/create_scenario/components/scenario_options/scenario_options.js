import "./scenario_options.css";
import React, { useContext, useState, useEffect } from 'react';

import Container from 'react-bootstrap/Container'; 
import Row from 'react-bootstrap/Row'; 
import Col from 'react-bootstrap/Col'; 
import Button from 'react-bootstrap/Button'
import { CreateScenarioContext } from '../../src/create_scenario';

export default function scenario_options() {
     const { typeSelection, setTypeSelection } = useContext( CreateScenarioContext );
     const setScenario = (e) => {
          setTypeSelection("ASGGjchabsbcwkb")
     };  

     const scenario_dict = [[{Difficulty:"e", Scenario:"Getting Started"}, {Difficulty:"e", Scenario:"File Wrangler"}],
     
     [{Difficulty:"m", Scenario:"Elf Infection"}, {Difficulty:"m", Scenario:"Strace"}, {Difficulty:"m", Scenario:"Treasure Hunt"}],

     [{Difficulty:"m", Scenario:"SSH Inception"}, {Difficulty:"m", Scenario:"Total Recon"}, {Difficulty:"m", Scenario:"Webfu"}],
     [{Difficulty:"h", Scenario:"Metasploitable"}]];

  return (
    <div>
     <h1>{typeSelection}</h1>  
     <h1>Choose Scenario</h1>
     <Container> 
      <h3></h3>
          {scenario_dict.map((scenario_row, row_num) => (
               <Row key={row_num}>
              {scenario_row.map((scenario, index) => (
                    <Col key={index}>
                    <Button onClick={setScenario} className={scenario.Difficulty}>{scenario.Scenario}</Button>
                    </Col> 
               ))}  
               </Row>
          ))}        
     </Container>     
    </div>
    
  )
}
