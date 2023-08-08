import React, { useState, useEffect, useContext } from 'react';
import './NewDash.css';
import { MainFrameContext } from '../../../main_frame/MainFrame';
import { Link, Route, Routes } from 'react-router-dom';
import Scenarios from '../scenarios/Scenarios';
import  '../../../../scripts/ui/navItemsData'
import { 
    DashSideNav_logged_out, 
    DashSideNav_student_logged_in,
    DashSideNav_instructor_logged_in, 
    DashSideNav_admin_logged_in, 
} from '../../../../scripts/ui/navItemsData';
import DevTable from '../../../main_frame/components/temp/DevTable';
import InstructorDash from '../instructor/InstructorDash';
import AdminDash from '../admin/AdminDash';
import DashHome from './DashHome';
import SSHmodal from '../ssh/SSHmodal';
import Users from '../users/Users';
import UserGroups from '../users/UserGroups';
import ScenarioGroups from '../scenarios/ScenarioGroups';
import DashNotifications from '../notifications/components/DashNotifications';
import Account from '../account/Account';

function DashRouter (    ) {

    const   { login_state } = useContext(MainFrameContext);
    
    const dataType = Object.freeze({
        USERS: 0,
        USER_GROUPS: 1,
        SCENARIOS: 2,
        SCENARIO_GROUPS: 3
    });
    
    const navDataToShow = login_state === 1 ? DashSideNav_admin_logged_in : DashSideNav_logged_out; // needs update for permissions!  ***************

    return (
        
        <div className='newdash-frame'>
            <div className='newdash-frame-carpet'>

                    <div className='newdash-sidebar-frame'>
                        {navDataToShow.map((val,key) => {
                            return (
                                <Link to={val.path} key={key}>
                                <li className='newdash-sidebar-row'>
                                        <div id='newdash-sidebar-icon'>{val.icon}</div>
                                        <div id='newdash-sidebar-title'>{val.title}</div>
                                    </li>
                                </Link>
                            );
                        })}
                        
                    </div>

                        <div className="newdash-infopane-frame">
                        <div className='newdash-infopane-content'>
                            <Routes>
                                <Route path="/*" element={<DashHome />} />
                                <Route path="/admin/*" element={<AdminDash />} />
                                <Route path="/instructor/*" element={<InstructorDash />} />
                                <Route path="/account" element={<Account />} />
                                <Route path="/users" element={<Users />} />
                                <Route path="/userGroups" element={<UserGroups />} />
                                <Route path="/scenarios" element={<Scenarios />} />
                                <Route path="/scenarioGroups" element={<ScenarioGroups />} />
                                <Route path="/notifications" element={<DashNotifications />} />
                                <Route path="/ssh" element={<SSHmodal />} />
                                <Route path="/devtable" element={<DevTable />} />
                            </Routes>
                        </div>            
                    </div>
            </div>
        </div>
    );
}

export default DashRouter;
