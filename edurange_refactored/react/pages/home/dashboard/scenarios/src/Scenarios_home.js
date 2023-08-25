import React, {useContext} from 'react';

import '../../src/Dashboard.css'
import './Scenarios_home.css'

import { HomeRouterContext } from '../../../src/Home_router';
import Login from '../../../src/components/login/Login';
import ScenarioTable from './components/list/ScenarioTable';

function Scenarios_home () {
    
    const { userData_state } = useContext( HomeRouterContext ); 
    if (!userData_state.username) {
        return ( <Login/> )
    }
    
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
