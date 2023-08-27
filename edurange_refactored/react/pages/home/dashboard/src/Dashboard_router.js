
import React, { useContext } from 'react';
import { Link, Route, Routes } from 'react-router-dom';
import { HomeRouterContext } from '../../src/Home_router';
import Dashboard_home from './Dashboard_home';
import DashSidebar from './sidebar/DashSidebar';
import JWT_Test from '../src/components/JWT_test';

import './Dashboard.css';
import Logout from '../../src/components/logout/Logout';
import { DashSideNav_admin_logged_in, DashSideNav_logged_out } from '../../../../modules/nav/navItemsData';
import Scenarios_router from '../scenarios/src/Scenarios_router';

function Dashboard_router() {

  const { login_state } = useContext(HomeRouterContext);
  const navDataToShow = (login_state) ? DashSideNav_admin_logged_in  : DashSideNav_logged_out;

  // these routes extend /edurange3/dashboard
  // e.g. scenarios is URL /edurange3/dashboard/scenarios
  return (

    <div className='newdash-frame'>
      <div className='newdash-frame-carpet'>

        <DashSidebar navDataToShow={navDataToShow} />

        <div className="newdash-infopane-frame">
          <div className='newdash-infopane-content'>
            <Routes>
              <Route path="/*" element={<Dashboard_home />} />
              <Route path="/scenarios/*" element={<Scenarios_router />} />
              <Route path="/jwt_test" element={<JWT_Test />} />
              <Route path="/logout" element={<Logout />} />

              {/* <Route path="/admin/*" element={<AdminDash />} /> */}
              {/* <Route path="/instructor/*" element={<InstructorDash />} /> */}
              {/* <Route path="/account" element={<Account />} /> */}
              {/* <Route path="/users" element={<Users />} /> */}
              {/* <Route path="/userGroups" element={<UserGroups />} /> */}
              {/* <Route path="/scenarios" element={<Scenarios_home />} /> */}
              {/* <Route path="/scenarios/:uid/:pageID" element={<ScenarioFullView />}/> */}
              {/* <Route path="/scenarioGroups" element={<ScenarioGroups />} /> */}
              {/* <Route path="/notifications" element={<DashNotifications />} /> */}
              {/* <Route path="/ssh" element={<SSHmodal />} /> */}

            </Routes>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard_router;
