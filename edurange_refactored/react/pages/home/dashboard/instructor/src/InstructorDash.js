import React, { useState } from 'react';

import { scenarioShells } from '../../../../../modules/shells/scenarioType_shells';
import Instructor_ScenTable from './Instructor_ScenTable';
import axios from 'axios';
import Instructor_ScenDetail from './Instructor_ScenDetail';

function InstructorDash() {

  // CREATE NEW SCENARIO GROUP 

  // State of desired name input field for adding NEW ScenarioGroup to db
  // IMPORTANT! (not to be confused with the name of currently existing scen group that is used as arg for create_scenario!)
  const [newScenGroup_name_state, set_newScenGroup_name_state] = useState('');
  
  const handle_newGroup_name_change = (event) => {
    set_newScenGroup_name_state(event.target.value);
  };
  const handle_createGroup_submit = (event) => {
    event.preventDefault();
    axios.post('/api/create_group', {
      group_name: newScenGroup_name_state
    })
    .then(response => {
      console.log('Group created:', response.data);
      set_newScenGroup_name_state(''); // Reset the input field after submission
    })
    .catch(error => {
      console.error('Error creating group:', error);
    });
  };
  // NEW SCENARIOS
  // just for creating a new scenario, not updating
  const [newScenType_state, set_newScenType_state] = useState('');
  const [newScenName_state, set_newScenName_state] = useState('');
  
  // IMPORTANT! (not to be confused with desired name for NEW scen group that is used as arg for create_group!)
  const [newScen_groupName_state, set_newScen_groupName_state] = useState('');
  // state of scenario type selected, for new scenario creation
  const handle_scenTypebtn_change = (event) => {
    set_newScenType_state(event.target.value);
  };
  const handle_scenName_change = (event) => {
    set_newScenName_state(event.target.value);
  };
  const handle_groupName_change = (event) => {
    set_newScen_groupName_state(event.target.value);
  };
  const handle_createScenario_submit = (event) => {
    event.preventDefault();
    console.log('submit clicked')
    axios.post('/api/scenario_interface', {
      METHOD:'CREATE',
      type: newScenType_state,
      name: newScenName_state,
      group_name: newScen_groupName_state
    })
  };
  
  // EXISTING SCENARIOS
  // state of info for currently selected scenario (previously created), from instructor table
  const [scenarioDetail_state, set_scenarioDetail_state] = useState({})

  return (
    <>
      <div className="group-creation-container">
        <form onSubmit={handle_createGroup_submit}>
          <input
            type="text"
            className="group-input"
            placeholder="Enter new group name"
            value={newScenGroup_name_state}
            onChange={handle_newGroup_name_change}
          />
          <button type="submit" className="group-submit-btn">Create Group</button>
        </form>
      </div>


    <Instructor_ScenDetail scenario_detail={scenarioDetail_state}/>
    <Instructor_ScenTable set_scenarioDetail_state={set_scenarioDetail_state}/>
    New Scenario Type:
      <form onSubmit={handle_createScenario_submit}>
        {Object.keys(scenarioShells).map((key) => {
          const scenario = scenarioShells[key];
          return (
            
            <div key={key}>
              <input
                type="radio"
                name="scenarioType"
                value={scenario.type}
                checked={newScenType_state === scenario.type}
                onChange={handle_scenTypebtn_change}
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
          value={newScenName_state}
          onChange={handle_scenName_change}
        />
        <br></br>
        <input
          type="text"
          placeholder="student group name"
          value={newScen_groupName_state}
          onChange={handle_groupName_change}
        />
        <button type="submit">Submit</button>
      </form>
    </>
  );
}

export default InstructorDash;
