/* This is the entry point for the parent component page and
* the super container for the other components.
*/


// Corresponding stylesheet, in the same folder as the component. 
//import "./Create_scenario.css";

//import Create_scenarioButton from "../Create_scenarioButton/Create_scenarioButton.js";
//import { createRoot } from 'react-dom/client';
import React, { useState, useEffect } from 'react';
//import ScenarioTable from "../ScenarioTable/ScenarioTable.js"
//import GroupSelector from "../new_scenario/group_selector/group_selector.js"
import ScenarioNameSelector from "../components/scenario_name_selector/scenario_name_selector.js"
//import CreateScenario from '../components/scenario_name_selector/scenario_name_selector.js';
//import ScenarioOptions from "../new_scenario/scenario_options/scenario_options.js"



// Your component should always begin with a capital letter.
function CreateScenario(props) {
       return (
              <>
                     <ScenarioNameSelector/>
              </>
       ); 
}


 {/*            <div id="Create_scenario">
                     <h1>Scenarios</h1>
	       	     <ScenarioTable/>
                     <Create_scenarioButton color="secondary"/>
       </div> */} 

export default CreateScenario;
