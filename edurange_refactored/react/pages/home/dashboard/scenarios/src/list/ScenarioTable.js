import axios from 'axios';
import React, { useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';

import './ScenarioTable.css';
import { ScenariosRouterContext } from '../Scenarios_router';

function ScenarioTable() {

    const navigate = useNavigate();

    const { scenarioList_state,   set_scenarioList_state,
            scenarioMeta_state, set_scenarioMeta_state
     } = useContext( ScenariosRouterContext );

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

    function handleNavClick (scenario_index) {
        const currentMeta = scenarioList_state[scenario_index];
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
            {scenarioList_state.slice(0).map((scenario, index) => (
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

export default ScenarioTable;