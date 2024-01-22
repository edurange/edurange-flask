import React, { useState } from 'react';

import { scenarioShells } from '../../../../../modules/shells/scenarioType_shells';
import Instructor_ScenTable from './Instructor_ScenTable';
import axios from 'axios';

function InstructorDash() {
    
  const [scenarioType_state, set_scenarioType_state] = useState('');
  const [scenarioName_state, set_scenarioName_state] = useState('');

  const handleRadioChange = (event) => {
    set_scenarioType_state(event.target.value);
  };

  const handleTextChange = (event) => {
    set_scenarioName_state(event.target.value);
  };

  // Function to handle form submission (you can add your fetch logic here)
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('submit clicked')
    axios.post('/api/scenario_interface', {
        METHOD:'CREATE',
        type: scenarioType_state,
        name: scenarioName_state
    })
    // Perform your fetch request here with scenarioType_state and scenarioName_state
  };

  return (
    <>
    <Instructor_ScenTable/>
    New Scenario Type:
      <form onSubmit={handleSubmit}>
        {Object.keys(scenarioShells).map((key) => {
          const scenario = scenarioShells[key];
          return (
            
            <div key={key}>
              <input
                type="radio"
                name="scenarioType"
                value={scenario.type}
                checked={scenarioType_state === scenario.type}
                onChange={handleRadioChange}
              />
              <label>{scenario.type}</label>
            </div>
          );
        })}
        New Scenario Name:
        <br></br>
        <input
          type="text"
          placeholder="scenario unique name"
          value={scenarioName_state}
          onChange={handleTextChange}
        />
        <button type="submit">Submit</button>
      </form>
    </>
  );
}

export default InstructorDash;
