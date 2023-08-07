import React, { useState, useEffect, useContext } from 'react';
import './NewDash.css';
import { MainFrameContext } from '../../../main_frame/MainFrame';
import { BrowserRouter as Link, Router, Route, Routes, Switch } from 'react-router-dom';
import Scenarios from '../scenarios/Scenarios';
import Accountmgmt from '../../../accountmgmt/components/main/Accountmgmt';

import Notifications from '../notifications/components/Notifications';

import DevTable from '../../../main_frame/components/temp/DevTable';
import InstructorDash from '../instructor/InstructorDash';
import AdminDash from '../admin/AdminDash';
import DashHome from './DashHome';
import SSHconnect from '../../../main_frame/components/sshConnect/SSHconnect';

function NewDash (    ) {

    const   {   activeTab_state,  update_tabChoice_status,
        login_state 
    } = useContext(MainFrameContext);
    
    const dataType = Object.freeze({
        USERS: 0,
        USER_GROUPS: 1,
        SCENARIOS: 2,
        SCENARIO_GROUPS: 3
    });
    
    // const navDataToShow = login_state === 1 ? DashSideNav_admin_logged_in : DashSideNav_logged_out; // needs update for permissions!  ***************

    return (
        
        <div className='newdash-frame'>
            <div className='newdash-frame-carpet'>

                    <div className='newdash-sidebar-frame'>
                    </div>

                        <div className="newdash-infopane-frame">
                        <div className='newdash-infopane-content'>
                            <Routes>
                                <Route path="/scenarios" element={<Scenarios />} />
                                <Route path="/*" element={<DashHome />} />
                                <Route path="/account" element={<Accountmgmt />} />
                                <Route path="/notifications" element={<Notifications />} />
                                <Route path="/ssh" element={<SSHconnect />} />
                                <Route path="/devtable" element={<DevTable />} />
                                <Route path="/admin/*" element={<AdminDash />} />
                                <Route path="/instructor/*" element={<InstructorDash />} />
                            </Routes>
                        </div>            
                    </div>
            </div>
        </div>
    );
}

export default NewDash;
