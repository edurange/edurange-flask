import axios from 'axios';
import React, { useEffect, useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import '../../scenarios/src/list/ScenarioTable.css';

function Instructor_ScenTable() {

    const [scenariosList_state, set_scenariosList_State] = useState([]);
    const navigate = useNavigate();
;

    async function fetchScenarioList() {
        try {
            const response = await axios.post("/api/scenario_interface",{METHOD: 'LIST'});
            console.log(response);
            if (response.data.scenarios_list) {
                set_scenariosList_State(response.data.scenarios_list);
            };
        }
        catch (error) {console.log('get_scenarios_list error:', error);};
    };
    useEffect(() => {fetchScenarioList();}, []);

    function handleNavClick (scenario_index) {
        const currentMeta = scenariosList_state[scenario_index];
        navigate(`${currentMeta.scenario_id}/0`);
    };



    return (
        <div className="newdash-datatable-frame">

            <div className="newdash-datatable-header">
                <div className='table-cell-item table-active' >ID</div>
                <div className='table-cell-item table-scenario-name'>Title</div>
                <div className='table-cell-item table-scenario-name'>Type</div>
                <div className='table-cell-item table-scenario-name'>Group</div>
                <div className='table-cell-item table-scenario-name'>Owner</div>
            </div>
            {scenariosList_state.slice(0).map((scenario, index) => (
                <div  key={scenario.scenario_id} onClick={() => handleNavClick(index)} >
                    <div className="table-row">
                        <div className='table-cell-item table-active'>{scenario.scenario_id}</div>
                        <div className='table-cell-item table-scenario-name'>{scenario.scenario_name}</div>
                        <div className='table-cell-item table-scenario-name'>{scenario.scenario_type}</div>
                        <div className='table-cell-item table-scenario-name'>{scenario.group_name}</div>
                        <div className='table-cell-item table-scenario-name'>{scenario.owner_name}</div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default Instructor_ScenTable;