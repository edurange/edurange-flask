import React from 'react';
import NewDash from '../main/NewDash';
import ScenarioGroupsTable_temp from './ScenarioGroupsTable_temp';
import '../main/NewDash.css'
const Scenarios_temp = () => {
    return (
        <div>
            <div className='dash-placard' >Scenarios</div>
            <ScenarioGroupsTable_temp/>
        </div>
    );
}

export default Scenarios_temp;
