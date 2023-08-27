"use strict";

import React, { useState } from 'react';
import { Route, Routes, useNavigate } from 'react-router-dom';

import './Home.css';

import Home from './Home';
import HomeHead from './components/frame/head/HomeHead';
import HomeFoot from './components/frame/foot/HomeFoot';
import Dashboard_router from '../dashboard/src/Dashboard_router';
import Login from './components/login/Login';
import Logout from './components/logout/Logout';
import InfoRouter from '../info/src/Info_router';

import { LoggedIn_context } from '../../../modules/context/LoggedIn_context';
import Options_controller from '../options/src/Options_controller';

export const HomeRouterContext = React.createContext();


function Home_router() {

  ////HOOKS//////////////////////////////////////
  const [userData_state, set_userData_state] = useState({});
  const [instructorData_state, set_instructorData_state] = useState({});
  // restores 'logged in' bool from session storage (superficial auth)
  const [login_state, set_login_state] = useState(() => {
    const edurange3_session_string = sessionStorage.getItem('edurange3_session');
    if (!edurange3_session_string) { return false; };
    const edurange3_session = JSON.parse(edurange3_session_string);
    const isLoggedIn = edurange3_session.isLoggedIn;
    const expiry = edurange3_session.expiry;
    if (isLoggedIn && Date.now() < expiry) { return true; }
    else { return false; };
  });
  //////////////////////////////////////////////


  // these routes extend the base URL of /edurange3/
  // e.g. dashboard is URL /edurange3/dashboard
  return (
    <div id='edurange-appframe'>

      <HomeRouterContext.Provider value={{
        userData_state, set_userData_state,
        login_state, set_login_state,
        instructorData_state, set_instructorData_state,
      }}>

        <HomeHead />

        <div id='edurange-content'>
          <div className='universal-content-outer'>
            <div className='universal-content-mid'>
              <div className='universal-content-inner'>
                <Routes>
                  <Route path="/edurange3/" element={<Home />} />
                  <Route path="/edurange3/login" element={<Login />} />
                  <Route path="/edurange3/logout" element={<Logout />} />
                  <Route path="/edurange3/options/*" element={<Options_controller />} />
                  <Route path="/edurange3/info/*" element={<InfoRouter />} />
                  <Route path="/edurange3/dashboard/*" element={
                    <LoggedIn_context>
                      <Dashboard_router />
                    </LoggedIn_context>
                  } />
                </Routes>
              </div>
            </div>
          </div>
        </div>

        <HomeFoot />

      </HomeRouterContext.Provider>
    </div>
  );
};

export default Home_router;
