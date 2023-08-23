
import React, { useContext } from 'react';
import { Link, Route, Routes } from 'react-router-dom';

// import InstructorDash from '../instructor/InstructorDash';
// import AdminDash from '../admin/AdminDash';
// import SSHmodal from '../ssh/SSHmodal';
// import Users from '../users/Users';
// import UserGroups from '../users/UserGroups';
// import ScenarioGroups from '../scenarios/ScenarioGroups';
// import DashNotifications from '../notifications/components/DashNotifications';
// import Account from '../account/Account';
// import ScenarioCardDetail from '../scenarios/ScenarioCardDetail';

import { HomeRouterContext } from '../../src/Home_router';
import './Dashboard.css';
import {
  DashSideNav_logged_out,
  DashSideNav_student_logged_in,
  DashSideNav_instructor_logged_in,
  DashSideNav_admin_logged_in,
  DashContextNav_admin_logged_in,
  DashContextNav_logged_out
} from '../../../../modules/nav/navItemsData';
import Dashboard_home from './Dashboard_home';
import Scenarios_home from '../scenarios/src/Scenarios_home';
import ScenarioFullView from '../scenarios/src/components/guide/ScenarioFullView';
import JWT_Test from './JWT_test';

function Dashboard_router() {

  const { login_state} = useContext(HomeRouterContext);

  // console.log("user is logged in: ",login_state)
  const navDataToShow = login_state === true ? DashSideNav_admin_logged_in : DashSideNav_logged_out; // needs update for permissions!  ***************
  return (

    <div className='newdash-frame'>
      <div className='newdash-frame-carpet'>

        <div className='newdash-sidebar-frame'>
          {navDataToShow.map((val, key) => {
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
              <Route path="/*" element={<Dashboard_home />} />
              {/* <Route path="/admin/*" element={<AdminDash />} /> */}
              {/* <Route path="/instructor/*" element={<InstructorDash />} /> */}
              {/* <Route path="/account" element={<Account />} /> */}
              {/* <Route path="/users" element={<Users />} /> */}
              {/* <Route path="/userGroups" element={<UserGroups />} /> */}
              <Route path="/scenarios" element={<Scenarios_home />} />
              {/* <Route path="/scenarios" element={<Scenarios_home />} /> */}
              <Route path="/scenarios/:uid/:pageID" element={<ScenarioFullView />}/>
              {/* <Route path="/scenarioGroups" element={<ScenarioGroups />} /> */}
              {/* <Route path="/notifications" element={<DashNotifications />} /> */}
              {/* <Route path="/ssh" element={<SSHmodal />} /> */}
              <Route path="/jwt_test" element={<JWT_Test  />} />
            </Routes>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard_router;
