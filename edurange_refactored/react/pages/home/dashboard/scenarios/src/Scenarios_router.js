

import React, { useContext, useState, useEffect } from 'react';
import { Link, Route, Routes } from 'react-router-dom';
import { HomeRouterContext } from '../../../src/Home_router';
import SSHmodal from '../../src/components/ssh/SSHmodal';
import Guide_controller from './guide/Guide_controller';
import Scenarios_home from './Scenarios_home';
import ScenarioChat from '../chat/src/ScenarioChat';
// import contentJSON from '../../../../../../../../../data/tmp/Facebooksploitable/student_view/content.json'
// import studentsJSON from '../../../../../../../../../data/tmp/Facebooksploitable/students.json'
// import studentsJSON from '../../../../../../../data/tmp/Facebooksploitable/students.json';

export const ScenariosRouterContext = React.createContext();

function Scenarios_router() {

///HOOKS//////////////////////////////////////
    const { login_state, userData_state } = useContext( HomeRouterContext );
    const [ scenarioList_state, set_scenarioList_state ] = useState([]);    
    const [ scenarioPage_state, set_scenarioPage_state ] = useState({
        chapter: "home",
        sectionAnchor: 0,
    });    
    const [ scenarioMeta_state, set_scenarioMeta_state ] = useState({
        scenario_id: null,
        scenario_name: null,
        scenario_type: null,
        group_name: null,
        owner_name: null,
    });
/////////////////////////////////////////////////



    return (
        <ScenariosRouterContext.Provider value={{ 
            scenarioList_state, set_scenarioList_state,
            scenarioPage_state, set_scenarioPage_state,
            scenarioMeta_state, set_scenarioMeta_state,
            }}>
            <Routes>
                <Route path="/" element={<Scenarios_home />} />
                <Route path="/:scenarioID" element={<Guide_controller />}/>
                <Route path="/:scenarioID/:pageID" element={<Guide_controller />}/>
                <Route path="/:scenarioID/chat" element={<ScenarioChat />}/>
                <Route path="/:scenarioID/ssh" element={<SSHmodal />}/>
                {/* <Route path="/:scenarioID/settings" element={<InstructorDash/>}/> */}
            </Routes>
        </ScenariosRouterContext.Provider>
    );
};

export default Scenarios_router;
