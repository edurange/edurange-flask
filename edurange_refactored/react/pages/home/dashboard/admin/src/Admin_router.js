


import axios from 'axios';
import React, { useContext, useState, useEffect } from 'react';
import { Route, Routes } from 'react-router-dom';
import { HomeRouterContext } from '../../../src/Home_router';
import Admin_home from './Admin_home';
import Admin_controller from './Admin_controller';
import ScenarioChat from '../../scenarios/chat/src/ScenarioChat';

export const AdminRouterContext = React.createContext();

function Admin_router() {

///HOOKS//////////////////////////////////////

    const { login_state, userData_state } = useContext( HomeRouterContext );

    const [ guideBook_state,    set_guideBook_state    ] = useState({});
    const [ guideContent_state, set_guideContent_state ] = useState({});
    const [ scenarioList_state, set_scenarioList_state ] = useState([]);    
    const [ scenarioPage_state, set_scenarioPage_state ] = useState({
        chapter: 0,
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
        <AdminRouterContext.Provider value={{ 
            scenarioList_state, set_scenarioList_state,
            scenarioPage_state, set_scenarioPage_state,
            guideBook_state,    set_guideBook_state,
            guideContent_state, set_guideContent_state
            }}>
            <Routes>
                <Route path="/" element={<Admin_home />} />
                <Route path="/:scenarioID" element={<Admin_controller />}/>
                <Route path="/:scenarioID/:pageID" element={<Admin_controller />}/>
                <Route path="/:scenarioID/chat" element={<ScenarioChat />}/>

            </Routes>
        </AdminRouterContext.Provider>
    );
};

export default Admin_router;
