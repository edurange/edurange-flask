import React, { useState, useEffect, useContext } from 'react';
import './NewDash.css';
import { MainFrameContext } from '../../../main_frame/MainFrame';
import { DashSideNav_admin_logged_in, DashSideNav_student_logged_in, DashSideNav_logged_out } from '../../../../scripts/routing/NavData';
function DashHome (    ) {

    const   {   activeTab_state,  update_tabChoice_status,
        login_state 
    } = useContext(MainFrameContext);
    
    const dataType = Object.freeze({
        USERS: 0,
        USER_GROUPS: 1,
        SCENARIOS: 2,
        SCENARIO_GROUPS: 3
    });
    
    const navDataToShow = login_state === 1 ? DashSideNav_admin_logged_in : DashSideNav_logged_out; // needs update for permissions!  ***************

    return (
        <>THIS IS THE HOME DASHBOARD PAGE! </>
    );
}

export default DashHome;
