
import React, { useContext } from 'react';
import { Link, Route, Routes } from 'react-router-dom';
import { HomeRouterContext } from '../../src/Home_router';
import Dashboard_home from './Dashboard_home';
import Scenarios_controller from '../scenarios/src/Scenarios_controller';
import CreateScenario from '../create_scenario/src/create_scenario';
import ScenarioDashboard from '../scenario_dashboard/src/scenario_dashboard';
import DashSidebar from './sidebar/DashSidebar';
import JWT_Test from '../src/components/JWT_test';



import './Dashboard.css';
import Logout from '../../src/components/logout/Logout';
import { DashSideNav_admin_logged_in, DashSideNav_logged_out } from '../../../../modules/nav/navItemsData';

function Dashboard_router() {

  const { login_state } = useContext(HomeRouterContext);
  const navDataToShow = (login_state) ? DashSideNav_admin_logged_in  : DashSideNav_logged_out;

  
  return (

    <div className='newdash-frame'>
      <div className='newdash-frame-carpet'>

        <DashSidebar navDataToShow={navDataToShow} />

        <div className="newdash-infopane-frame">
          <div className='newdash-infopane-content'>
            <Routes>
              <Route path="/*" element={<Dashboard_home />} />
              <Route path="/scenarios/*" element={<Scenarios_controller />} />
              <Route path="/jwt_test" element={<JWT_Test />} />
              <Route path="/logout" element={<Logout />} />

              {/* <Route path="/admin/*" element={<AdminDash />} /> */}
              {/* <Route path="/instructor/*" element={<InstructorDash />} /> */}
              {/* <Route path="/account" element={<Account />} /> */}
              {/* <Route path="/users" element={<Users />} /> */}
              {/* <Route path="/userGroups" element={<UserGroups />} /> */}
              {<Route path="/scenarios" element={<ScenarioDashboard />} />}
              {<Route path="/create_scenario" element={<CreateScenario />} />}
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
