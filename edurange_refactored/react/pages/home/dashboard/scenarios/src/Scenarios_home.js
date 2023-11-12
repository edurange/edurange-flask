import React, {useContext} from 'react';

import '../../src/Dashboard.css'
import './Scenarios_home.css'

import ScenarioTable from './list/ScenarioTable';
import { HomeRouterContext } from '../../../src/Home_router';

function Scenarios_home () {
    
    const { userData_state } = useContext( HomeRouterContext ); 
    
    return ( 
            <div className='scenario-home-outer-frame'>
                <div className='scenario-home-inner-frame'>
                    <div className='newdash-content-placard' >
                        Scenarios
                    </div>
                    < ScenarioTable />
                </div>
            </div>
    );
};
export default Scenarios_home;
