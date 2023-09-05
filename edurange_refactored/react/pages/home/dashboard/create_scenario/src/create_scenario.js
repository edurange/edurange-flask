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
    const [currentComponent, setCurrentComponent] = useState(2);

    // Context states for scenario creation
    const [typeIsSelected, setTypeIsSelected] = useState(false);
    const [groupIsSelected, setGroupIsSelected] = useState(false);
    const [nameIsSelected, setNameIsSelected] = useState(false);
    
    // Scenario context, to keep track of when each prompt response has been gathered
    // so createScenarioTask API call can be made to complete scenario creation. 
    const CreateScenarioContext = createContext();

    const clickHandler = () => {
        if (currentComponent != 3) {
            setCurrentComponent(currentComponent+1) 
         } 
    }

    return (
            <>
                <CreateScenarioContext.Provider value={{

                    typeIsSelected, setTypeIsSelected,
                    groupIsSelected, setGroupIsSelected,
                    nameIsSelected, setNameIsSelected,

                 }}>
                        {prompt_components[currentComponent]}
                        <Button onClick={clickHandler}>Next</Button>
                
                </CreateScenarioContext.Provider>
            </>
       ); 
}

export default CreateScenario;