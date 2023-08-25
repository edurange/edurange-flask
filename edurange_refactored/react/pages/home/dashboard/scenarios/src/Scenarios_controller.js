

import React, { useContext, useState, useEffect } from 'react';
import { Link, Route, Routes } from 'react-router-dom';


import SSHmodal from '../../src/components/ssh/SSHmodal';
import InstructorDash from '../../instructor/src/InstructorDash';
import ScenarioChat from '../chat/ScenarioChat';
import Scenarios_home from './Scenarios_home';
import { HomeRouterContext } from '../../../src/Home_router';
import ScenarioFullView from './components/guide/ScenarioFullView';

export const ScenarioControllerContext = React.createContext();

function Scenarios_controller() {

///HOOKS//////////////////////////////////////
    const { login_state, userData_state } = useContext( HomeRouterContext );
    const [ scenarioList_state,   set_scenarioList_state ]   = useState([]);    
//  const [ currentScenario_state,   set_currentScenario_state]   = useState({});    


    return (
        <ScenarioControllerContext.Provider value={{ scenarioList_state, set_scenarioList_state }}> 
            <Routes>
                <Route path="/" element={<Scenarios_home />} />
                <Route path="/:scenarioID" element={<ScenarioFullView />}/>
                <Route path="/:scenarioID/:pageID" element={<ScenarioFullView />}/>
                <Route path="/:scenarioID/chat" element={< ScenarioChat />}/>
                <Route path="/:scenarioID/ssh" element={<SSHmodal />}/>
                {/* <Route path="/:scenarioID/settings" element={<InstructorDash scenarioID={scenarioID} />}/> */}
            </Routes>
        </ScenarioControllerContext.Provider>
    );
};

export default Scenarios_controller;
