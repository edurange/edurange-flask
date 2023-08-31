import React, {useContext} from 'react';

import { HomeRouterContext } from '../../src/Home_router';
import Login from '../../src/components/login/Login';

function Dashboard_home () {
    
    const { userData_state } = useContext( HomeRouterContext ); 

    // if (!userData_state.username) { return <Login/> }

    const currentDate = new Date().toDateString();
    const currentTime = new Date().toLocaleTimeString();

    return (
        <div>
            Welcome, {userData_state.username}.
            The time is now {currentTime} on {currentDate}.
        </div>
    );
};
export default Dashboard_home;