
import React, { useContext } from 'react';
import { Link, Route, Routes } from 'react-router-dom';
import { HomeRouterContext } from '../../src/Home_router';
import Dashboard_home from './Dashboard_home';
import DashSidebar from './sidebar/DashSidebar';
import JWT_Test from '../src/components/JWT_test';

import './Dashboard.css';
import Scenarios_router from '../scenarios/src/Scenarios_router';
import { navArrays } from '../../../../modules/nav/navItemsData';
import AdminDash from '../admin/src/AdminDash';
import InstructorDash from '../instructor/src/InstructorDash';
import Account from '../account/src/Account';
import Logout from '../../src/components/logout/Logout';
import SSHmodal from './components/ssh/SSHmodal';
import DashNotifications from './components/notifications/components/DashNotifications';
import SSH_web from './components/ssh/SSH_web';

function Dashboard_router() {

  const { 
    login_state, set_login_state,
    navName_state, 
    userData_state, set_userData_state
  } = useContext(HomeRouterContext);
  
  
  const navLong = `side_${navName_state}`
  const navToShow = navArrays[navLong];
  
  // these routes extend /edurange3/dashboard
  // e.g. scenarios is URL /edurange3/dashboard/scenarios
  return (

    <div className='newdash-frame'>
      <div className='newdash-frame-carpet'>
      
        <DashSidebar navToShow={navToShow} />

        <div className="newdash-infopane-frame">
          <div className='newdash-infopane-content'>

            <Routes>
              <Route path="/*" element={<Dashboard_home />} />
              <Route path="/scenarios/*" element={<Scenarios_router />} />
              <Route path="/jwt_test" element={<JWT_Test />} />
              <Route path="/logout" element={<Logout />} />
              <Route path="/admin/*" element={<AdminDash />} />
              <Route path="/instructor/*" element={<InstructorDash />} />
              <Route path="/account" element={<Account />} />
              <Route path="/ssh" element={<SSHmodal />} />
              <Route path="/sshweb" element={<SSH_web />} />
              <Route path="/notifications" element={<DashNotifications />} />
            </Routes>

          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard_router;
