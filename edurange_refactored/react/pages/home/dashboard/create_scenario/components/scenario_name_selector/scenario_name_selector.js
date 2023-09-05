/*
    Final Step of Create Scenario proccess. 
    Component for inputting scenario name and notes.

*/

// Corresponding stylesheet, in the same folder as the component. 
import "./scenario_name_selector.css";

import React, { useState, useEffect } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';


// Your component should always begin with a capital letter.
export default function CreateScenario(props) {
    const [ scenarioName, setScenarioName] = useState("");
    const [ scenarioNotes, setScenarioNotes] = useState(""); 


    useEffect(() => {

    }, []);
  
    const handleScenarioNameInput = (data) => {
        // SLIME to-do: validate name input
        setScenarioName(data);
    }

    const handleScenarioNoteInput = (data) => {
        setScenarioNotes(data)
    }

    const submissionHandler = (data) => {
        // next page? new celery task?
    }


       return (
              <>
                     <h1>Select Scenario Name:</h1>
                   <Form>
                   
                        <Form.Group className="mb-3 scenarioName inputter" controlId="exampleForm.controlInput1">
                            <Form.Label>
                                Scenario Name
                            </Form.Label>
                            <Form.Control onChange={e => handleScenarioNameInput(e.target.value)}/>
                        </Form.Group>
                        
                        
                        <Form.Group className="mb-3" controlId="exampleForm.controlInput1" >
                            <Form.Label>
                                Notes: 
                            </Form.Label>
                            <Form.Control onChange={e => handleScenarioNoteInput(e.target.value)} as="textarea" rows={3}/>
                        </Form.Group>                        
                    </Form>     

              </>
       ); 
}



