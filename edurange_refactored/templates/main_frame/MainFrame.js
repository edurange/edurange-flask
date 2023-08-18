"use strict";

import React, { useState, useEffect} from 'react';
import { Route, Routes } from 'react-router-dom';
import { Auth_ContextProvider } from './Auth_ContextProvider';
import OptionsMenu from '../options/OptionsMenu';
import Login from './components/login/Login';
import FrameHead from './components/head/FrameHead';
import Logout_temp from './components/temp/Logout_temp';
import DashRouter from '../newDash/components/main/DashRouter';
import EduRangeHome from './components/home/EduRangeHome';
import InfoRouter from '../info/main/InfoRouter';
import FrameFoot from './components/foot/FrameFoot';

import '../../../assets/css/pucs.css'; // - Project Unified Custom Styles (pucs.css) cancels out and effectively replaces the original 'styles.css' from the legacy UI
import './MainFrame.css'; // styling specific to the mainframe component.  It is important that component-specific styling like this come AFTER the 'pucs.css' import.

export const MainFrameContext = React.createContext();
function MainFrame() {
  
  const connectIP = "127.0.0.1";
  const connectPort = "5000"; // or whatever your normal port is
  const loginRoute = "/home_sister/login"
  
  ////HOOKS//////////////////////////////////////
    const [ session_csrfToken_state,       set_session_csrfToken_state]       = useState(null);
    const [ session_userData_state,        set_session_userData_state]        = useState({});
    const [ session_instructorData_state,  set_session_instructorData_state]  = useState({});
    const [ jwt_authenticated_state,       set_jwt_authenticated_state]       = useState(false)
///////////////////////////////////////////////

// Will get initial CSRF token upon page load 
useEffect(() => {
  async function fetch_csrfToken () {
    try {
      const metaTag = document.querySelector('meta[name="csrf_token_sister"]');
      if (metaTag) { set_session_csrfToken_state (metaTag.content); }
    } catch (error) {
      console.error('Unable to fetch CSRF token.', error);
    }

  };
  fetch_csrfToken();
}, [  ]);

return (
    <div id='edurange-appframe'>

      <MainFrameContext.Provider value={{

                connectIP, connectPort, loginRoute,

                session_csrfToken_state,      set_session_csrfToken_state,
                session_userData_state,       set_session_userData_state,
                session_instructorData_state, set_session_instructorData_state,
                jwt_authenticated_state,      set_jwt_authenticated_state

            }}>
              
          <FrameHead />
          <div id='edurange-content'>
            <div className='universal-content-outer'>
              <div className='universal-content-mid'>
                <div className='universal-content-inner'>
                  <Routes>
                    <Route path="/home_sister/" element={<EduRangeHome />} />
                    <Route path="/home_sister/login" element={<Login />} />
                    <Route path="/home_sister/logout" element={<Logout_temp />} />
                    <Route path="/home_sister/options" element={<OptionsMenu />} />
                    <Route path="/home_sister/info/*" element={<InfoRouter />} />
                      <Route path="/home_sister/dashboard/*" element={
                        <Auth_ContextProvider>
                          <DashRouter />
                        </Auth_ContextProvider>
                      } />
                  </Routes>
                </div>
              </div>
            </div>
          </div>
        <FrameFoot />
      </MainFrameContext.Provider>
    </div>
  );
}

export default MainFrame;
