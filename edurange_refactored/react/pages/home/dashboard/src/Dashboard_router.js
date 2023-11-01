
import React, { useContext, useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import { navArrays } from '../../../../modules/nav/navItemsData';
import { HomeRouterContext } from '../../src/Home_router';
import Dashboard_home from './Dashboard_home';
import SideNav from './sidenav/SideNav';
import JWT_Test from '../src/components/JWT_test';
import Scenarios_router from '../scenarios/src/Scenarios_router';
import Account from '../account/src/Account';
import Logout from '../../src/components/logout/Logout';
import AdminDash from '../admin/src/AdminDash';
import InstructorDash from '../instructor/src/InstructorDash';
import DashNotifications from './components/notifications/components/DashNotifications';
export const DashRouterContext = React.createContext();

import './Dashboard.css';

function Dashboard_router() {

  const { 
    login_state, set_login_state,
    navName_state,
    userData_state, set_userData_state
  } = useContext(HomeRouterContext);

  const fakeNotif= {
    id: 123,
    timeStamp: Date.now(),
    message: "something"
  }


  
  const [notifsArray_state, set_notifsArray_state] = useState([fakeNotif]);
  
  const navLongname = `side_${navName_state}`
  const navToShow = navArrays[navLongname];
  
  // these routes extend /edurange3/dashboard
  // e.g. scenarios is URL /edurange3/dashboard/scenarios
  return (

    <div className='newdash-frame'>
      <div className='newdash-frame-carpet'>
      <DashRouterContext.Provider value={{
        notifsArray_state, set_notifsArray_state
      }}>
      
        <SideNav navToShow={navToShow} smallMode={true} hiddenMode={false} />

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
              <Route path="/notifications" element={<DashNotifications notifsArray={notifsArray_state}/>} />
            </Routes>

          </div>
        </div>
        </DashRouterContext.Provider>
      </div>
    </div>
  );
}

export default Dashboard_router;
