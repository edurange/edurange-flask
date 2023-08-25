import axios from 'axios';
import React, { useEffect, useState, useContext } from 'react';
import { Link } from 'react-router-dom';

import '../../../../src/Dashboard.css'
import '../../../../src/tables.css'
import { ScenarioControllerContext } from '../../Scenarios_controller';

function ScenarioTable() {

    const { scenarioList_state,   set_scenarioList_state } = useContext( ScenarioControllerContext );

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

    console.log ("fetched list: ", scenarioList_state)

    return (
        <div className="newdash-datatable-frame">
            <div className="newdash-datatable-header">
                <div className='table-cell-item table-active' >ID</div>
                <div className='table-cell-item table-scenario-name'>Title</div>
                <div className='table-cell-item table-scenario-name'>Type</div>
                <div className='table-cell-item table-scenario-name'>Group</div>
                <div className='table-cell-item table-scenario-name'>Owner</div>
                {/* <div className='table-cell-item table-active' >Owner</div>
                <div className='table-cell-item table-active' >Status</div>
                <div className='table-cell-item table-created'>Created</div> */}
            </div>
            {scenarioList_state.slice(0).map((scenario) => (
                <Link key={scenario.scenario_id} to ={`${scenario.scenario_id}/home`}>
                    <div className="table-row">
                        <div className='table-cell-item table-active'>{scenario.scenario_id}</div>
                        <div className='table-cell-item table-scenario-name'>{scenario.scenario_name}</div>
                        <div className='table-cell-item table-scenario-name'>{scenario.scenario_type}</div>
                        <div className='table-cell-item table-scenario-name'>{scenario.group_name}</div>
                        <div className='table-cell-item table-scenario-name'>{scenario.owner_name}</div>
                        {/* <div className='table-cell-item table-active'>{scenario.ownerID}</div>
                        <div className='table-cell-item table-active'>{scenario.status ? "true":"false"}</div>
                        <div className='table-cell-item table-created'>{scenario.created_at}</div> */}
                    </div>
                </Link>
            ))}
        </div>
    );
}

export default ScenarioTable;