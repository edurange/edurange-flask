/* This is the entry point for the parent component page and
* the super container for the other components.
*/


// Corresponding stylesheet, in the same folder as the component. 
import "./ChooseScenario.css";
import Container from './Container';
import Table from './Table';

import { createRoot } from 'react-dom/client';
import React, { useState, useEffect } from 'react';
import { Container } from "react-bootstrap";

const scenarios = [{ name: 'Scenario 1', description: 'Description here' }, { name: 'Scenario 2', description: 'Description here' }];

// Your component should always begin with a capital letter.
function ChooseScenario() {
       return (
              <Container>
                     <h1>Choose a Scenario to Create</h1>
                     <Table scenarios={scenarios} />
              </Container>
       );
}


export default ChooseScenario;