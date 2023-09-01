
import axios from 'axios';
import React, { useContext, useState, useEffect } from 'react';
import { Link, Route, Routes } from 'react-router-dom';
import { HomeRouterContext } from '../../../src/Home_router';
import SSHmodal from '../../src/components/ssh/SSHmodal';
import Scenarios_home from './Scenarios_home';
import ScenarioChat from '../chat/src/ScenarioChat';
import ScenarioFullView from './guide/ScenarioFullView';

export const ScenariosRouterContext = React.createContext();

function Scenarios_router() {

///HOOKS//////////////////////////////////////

    const { login_state, userData_state } = useContext( HomeRouterContext );

    const [ guideBook_state,    set_guideBook_state    ] = useState({});
    const [ guideContent_state, set_guideContent_state ] = useState({});
    const [ scenarioList_state, set_scenarioList_state ] = useState([]);    
    const [ scenarioPage_state, set_scenarioPage_state ] = useState({
        chapter: "home",
        sectionAnchor: 0,
    });    
    const [ guideMeta_state,    set_guideMeta_state ] = useState({
        created_at: null,
        scenario_description: null,
        scenario_id: null,
        group_name: null,
        scenario_owner_id: null,
        scenario_status: null,
    });
    
/////////////////////////////////////////////////

    async function fetchScenarioList() {
        try {
            const response = await axios.get("/api/get_scenarios");
            if (response.data.scenarioTable) {
                set_scenarioList_state(response.data.scenarioTable);
            };
        }
        catch (error) {console.log('get_scenarios_list error:', error);};
    };
    useEffect(() => {fetchScenarioList();}, []);

    return (
        <ScenariosRouterContext.Provider value={{ 
            scenarioList_state, set_scenarioList_state,
            scenarioPage_state, set_scenarioPage_state,
            guideBook_state,    set_guideBook_state,
            guideContent_state, set_guideContent_state
            }}>
            <Routes>
                <Route path="/" element={<Scenarios_home />} />
                <Route path="/:scenarioID" element={<ScenarioFullView />}/>
                <Route path="/:scenarioID/:pageID" element={<ScenarioFullView />}/>
                <Route path="/:scenarioID/chat" element={<ScenarioChat />}/>
                <Route path="/:scenarioID/ssh" element={<SSHmodal />}/>
                {/* <Route path="/:scenarioID/settings" element={<InstructorDash/>}/> */}
            </Routes>
        </ScenariosRouterContext.Provider>
    );
};

export default Scenarios_router;
