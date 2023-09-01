/* This is the entry point for the parent component page and
* the super container for the other components.
*/


// Corresponding stylesheet, in the same folder as the component. 
//import "./Create_scenario.css";

import React, { useContext, useState, useEffect } from 'react';
import GroupSelector from "../components/group_selector/group_selector.js"
import ScenarioNameSelector from "../components/scenario_name_selector/scenario_name_selector.js"
import ScenarioOptions from "../components/scenario_options/scenario_options.js";
import Button from 'react-bootstrap/Button'





// Your component should always begin with a capital letter.
function CreateScenario(props) {
    const prompt_components = [<ScenarioOptions/>, <ScenarioNameSelector/>, <GroupSelector/>, <h1>Your Scenario Is Created!!!</h1>]; 
    const [currentComponent, setCurrentComponent] = useState(2);
    
    const clickHandler = () => {
        if (currentComponent != 3) {
            setCurrentComponent(currentComponent+1) 
         } 
    }

    return (
              <>
                    {prompt_components[currentComponent]}
                    <Button onClick={clickHandler}>Next</Button>
              </>
       ); 
}

export default CreateScenario;