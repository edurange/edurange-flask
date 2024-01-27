import React, { useState } from 'react';

import { scenarioShells } from '../../../../../modules/shells/scenarioType_shells';
import Instructor_ScenTable from './Instructor_ScenTable';
import axios from 'axios';
import Instructor_ScenDetail from './Instructor_ScenDetail';

function InstructorDash() {
    
  const [scenarioType_state, set_scenarioType_state] = useState('');
  const [scenarioName_state, set_scenarioName_state] = useState('');
  const [scenGroup_name_state, set_scenGroup_name_state] = useState('');
  const [scenarioDetail_state, set_scenarioDetail_state] = useState({})


  const handleRadioChange = (event) => {
    set_scenarioType_state(event.target.value);
  };

  const handle_scenNameChange = (event) => {
    set_scenarioName_state(event.target.value);
  };
  const handle_groupNameChange = (event) => {
    set_scenGroup_name_state(event.target.value);
  };

  // Function to handle form submission (you can add your fetch logic here)
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('submit clicked')
    axios.post('/api/scenario_interface', {
        METHOD:'CREATE',
        type: scenarioType_state,
        name: scenarioName_state,
        group_name: scenGroup_name_state
    })
    // Perform your fetch request here with scenarioType_state and scenarioName_state
  };

  return (
    <>
    <Instructor_ScenDetail scenario_detail={scenarioDetail_state}/>
    <Instructor_ScenTable set_scenarioDetail_state={set_scenarioDetail_state}/>
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
          onChange={handle_scenNameChange}
        />
        <br></br>
        <input
          type="text"
          placeholder="student group name"
          value={scenGroup_name_state}
          onChange={handle_groupNameChange}
        />
        <button type="submit">Submit</button>
      </form>
    </>
  );
}

export default InstructorDash;
