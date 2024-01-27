import axios from 'axios';
import React, { useEffect, useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import '../../scenarios/src/list/ScenarioTable.css';

function Instructor_ScenTable({set_scenarioDetail_state}) {

    const [scenariosList_state, set_scenariosList_state] = useState([]);
    const navigate = useNavigate();
;

    async function fetchScenarioList() {
        try {
            const response = await axios.post("/api/scenario_interface",{METHOD: 'LIST'});
            console.log(response);
            if (response.data.scenarios_list) {
                set_scenariosList_state(response.data.scenarios_list);
            };
        }
        catch (error) {console.log('get_scenarios_list error:', error);};
    };
    useEffect(() => {fetchScenarioList();}, []);

    function handleInspectClick (scenario_index) {

        set_scenarioDetail_state(scenariosList_state[scenario_index])
        // navigate(`${currentMeta.scenario_id}/0`);
    };
    function handleStartClick (scenario) {
        axios.post('/api/scenario_interface',{
            METHOD: 'START',
            scenario_id: scenario.scenario_id
        }
        )
    };
    function handleStopClick (scenario) {
        axios.post('/api/scenario_interface',{
            METHOD: 'STOP',
            scenario_id: scenario.scenario_id
        }
        )
    };
    function handleDestroyClick (scenario) {
        axios.post('/api/scenario_interface',{
            METHOD: 'DESTROY',
            scenario_id: scenario.scenario_id
        }
        )
    };



    return (
        <div className="newdash-datatable-frame">

            <div className="newdash-datatable-header">
                <div className='table-cell-item table-active' >ID</div>
                <div className='table-cell-item table-scenario-name'>Name</div>
                <div className='table-cell-item table-scenario-name'>Type</div>
                <div className='table-cell-item table-scenario-name'>Status</div>
                <div className='table-cell-item table-scenario-name'>CONTROL PANEL</div>
            </div>
            {scenariosList_state.slice(0).map((scenario, index) => (
                <div  key={scenario.scenario_id} onClick={() => handleInspectClick(index)} >
                    <div className="table-row">
                        <div className='table-cell-item table-active'>{scenario.scenario_id}</div>
                        <div className='table-cell-item table-scenario-name'>{scenario.scenario_name}</div>
                        <button onClick={() => handleStartClick(scenario)}>START</button>
                        <button onClick={() => handleStopClick(scenario)}>STOP</button>
                        <button onClick={() => handleDestroyClick(scenario)}>DESTROY</button>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default Instructor_ScenTable;