/* This is the entry point for the parent component page and
* the super container for the other components.
*/


// Corresponding stylesheet, in the same folder as the component. 
import "./CreateScenario.css";

import CreateScenarioButton from "../CreateScenarioButton/CreateScenarioButton.js";
import { createRoot } from 'react-dom/client';
import React, { useState, useEffect } from 'react';
import ScenarioTable from "../ScenarioTable/ScenarioTable.js"
import GroupSelector from "../new_scenario/group_selector/group_selector.js"
import ScenarioNameSelector from "../new_scenario/scenario_name_selector/scenario_name_selector.js"
import ScenarioOptions from "../new_scenario/scenario_options/scenario_options.js"



// Your component should always begin with a capital letter.
function CreateScenario(props) {
       return (
              <>
              <h1>"Scenario Options"</h1>
              <ScenarioOptions />
              </>
       ); 
}


 {/*            <div id="createScenario">
                     <h1>Scenarios</h1>
	       	     <ScenarioTable/>
                     <CreateScenarioButton color="secondary"/>
       </div> */} 

var e = document.getElementById('createScenario'); // The id assigned in html file. 
const root = createRoot(e);

root.render(<CreateScenario />);
