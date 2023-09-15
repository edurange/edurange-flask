/* This is the entry point for the parent component page and
* the super container for the other components.
*/


// Corresponding stylesheet, in the same folder as the component. 
//import "./Create_scenario.css";

import React, { createContext, useState, useEffect } from 'react';
import GroupSelector from "../components/group_selector/group_selector.js"
import ScenarioNameSelector from "../components/scenario_name_selector/scenario_name_selector.js"
import ScenarioOptions from "../components/scenario_options/scenario_options.js";
import Button from 'react-bootstrap/Button'


import axios from 'axios';
// Scenario context, to keep track of when each prompt response has been gathered
// so createScenarioTask API call can be made to complete scenario creation. 
export const CreateScenarioContext = createContext();

// Your component should always begin with a capital letter.
function CreateScenario(props) {
    
    // Components are rendered in sequence
    const prompt_components = [
        <ScenarioOptions/>, 
        <ScenarioNameSelector/>, 
        <GroupSelector/>, 
        <h1>Your Scenario Is Created!!!</h1>
    ]; 

    // State managing currently displayed component
    const [currentComponent, setCurrentComponent] = useState(0);

    // Context states for scenario creation
    const [typeSelection, setTypeSelection] = useState("");
    const [groupNameSelection, setGroupNameSelection] = useState("");
    const [scenarioNameSelection, setScenarioNameSelection] = useState("");
    



    const clickHandler = () => {
        // SLIME to do - remove button when we've reached the final component. 
        if (currentComponent != 3) {
            setCurrentComponent(currentComponent+1) 
         } 
    }



  async function doThing() {
    try {
    const username_input = "pumpernickel";
    const password_input = "pumpernickelz";
      const response = await axios.post('/api/make_scenario',
        {
          scenario_name: username_input,
          password: password_input
        }
      );
    const responseData = response.data;
    console.log(response.data);
      if (responseData.user_data) {
      console.log(':(');
        }
     
    } catch (error) {
      console.error('Error:', error);
    };
  }

  const thingFunc = () => { doThing(); }


    

    return (
            <>
            <h1>scenario name selection: {scenarioNameSelection}</h1>
            <Button onClick={thingFunc}>PRESS ME NOW</Button>
            
            <h1>group name: {groupNameSelection}</h1>
            <h1>type: {typeSelection}</h1>
                <CreateScenarioContext.Provider value={{

                    typeSelection, setTypeSelection,
                    groupNameSelection, setGroupNameSelection,
                    scenarioNameSelection, setScenarioNameSelection,

                 }}>
                        {prompt_components[currentComponent]}
                        <Button onClick={clickHandler}>Next</Button>
                
                </CreateScenarioContext.Provider>
            </>
       ); 
}

export default CreateScenario;