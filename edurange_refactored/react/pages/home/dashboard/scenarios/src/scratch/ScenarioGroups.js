import React from 'react';
import ScenarioGroupsTable from './ScenarioGroupsTable';
import '../main/NewDash.css'
function ScenarioGroups () {
    return (
        <div>
            <div className='newdash-content-placard' >Scenario Groups</div>
            <ScenarioGroupsTable/>
        </div>
    );
}

export default ScenarioGroups;
