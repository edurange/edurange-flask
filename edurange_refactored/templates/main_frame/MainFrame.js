"use strict";

import React, { useState, useEffect} from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import OptionsMenu from '../options/OptionsMenu';
import LoginFromNav from './components/login_from_nav/LoginFromNav';
import FrameHead from './components/head/FrameHead';
import Logout_temp from './components/temp/Logout_temp';
import DashRouter from '../newDash/components/main/DashRouter';
import EduRangeHome from './components/home/EduRangeHome';
import InfoRouter from '../info/main/InfoRouter';
import FrameFoot from './components/foot/FrameFoot';

import '../../../assets/css/pucs.css'
import './MainFrame.css';

export const MainFrameContext = React.createContext();

function MainFrame() {
  
    const connectIP = "127.0.0.1";
    const connectPort = "8008";
    const loginRoute = "/home_sister/login"

////HOOKS//////////////////////////////////////
    const [activeTab_state, set_activeTab_state] = useState(1);
    const [new_tabChoice_status, update_tabChoice_status] = useState(1);

    const [csrfToken_state, set_csrfToken_state] = useState(null);
    const [new_csrfToken_status, update_csrfToken_status] = useState(null);

    const [login_state, set_login_state] = useState(0);
    const [new_login_status, update_login_status] = useState(0);

    const [session_userInfo_state, set_session_userInfo_state] = useState({});
    const [session_instructorData_state, set_session_instructorData_state] = useState({});

    useEffect(() =>  {set_activeTab_state(new_tabChoice_status);}, [new_tabChoice_status]); 
    useEffect(() =>  {set_csrfToken_state(new_csrfToken_status);}, [new_csrfToken_status]); 
    useEffect(() =>  {set_login_state(new_login_status);}, [new_login_status]); 
/////////////////////////////////////////////


useEffect(() => {
  const fetch_csrfToken = async () => {
    try {
      const metaTag = document.querySelector('meta[name="csrf_token_sister"]');
      if (metaTag) {set_csrfToken_state (metaTag.content);}
    } catch (error) {
      console.error('Error fetching CSRF token:', error);
    }
  };
  fetch_csrfToken();
}, []);
// console.log(csrfToken_state);   // for debug

return (
    <div id='edurange-appframe'>
      <MainFrameContext.Provider value={{
                activeTab_state,    update_tabChoice_status,
                login_state,        update_login_status,
                csrfToken_state,
                connectIP, connectPort, loginRoute,
                session_userInfo_state, set_session_userInfo_state,
                session_instructorData_state, set_session_instructorData_state,
            }}>
          <FrameHead />
          <div id='edurange-content'>
            <div className='universal-content-outer'>
              <div className='universal-content-mid'>
                <div className='universal-content-inner'>
                  <Routes>
                    <Route path="/home_sister/" element={<EduRangeHome />} />
                    <Route path="/home_sister/login" element={<LoginFromNav />} />
                    <Route path="/home_sister/logout" element={<Logout_temp />} />
                    <Route path="/home_sister/options" element={<OptionsMenu />} />
                    <Route path="/home_sister/dashboard/*" element={<DashRouter />} />
                    <Route path="/home_sister/info/*" element={<InfoRouter />} />
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
// const entryPoint = document.getElementById('react-entry-id');
// const root=createRoot(entryPoint);
// root.render(<MainFrame/>);

    // The state hooks in this component are paired so one can act as a trigger for the other w/ useEffect
    // which can help prevent some render problems and allow for increased flexibility in how to handle
    // implementation of useEffect-triggered functions, while reducing confusion as to whether a state-setter
    // is actually changing state or calling a function. the following convention will help clarify.

    // Convention and state update flow: 
    //   - The *_state* variables are the main states, and their *set_* partners are ***useEffect only***
    //   - The *update_* function calls are used to update the *_status* variables
    //   - When a *_status* variable changes, that triggers a useEffect update from context provider component
    //   - This matching useEffect update then calls the actual *set_* function using the *_status* value as an argument.
    //   - The *set_* function then finally updates the original *_state* variable to match the *_status* variable / arg.
    //
    //   To change state in normal calls, the *update_* function should be used, not the *set_*
    //   which means that when passing down a 'setter' type function, always pass the *update_* version, 
    //   as well as the original *_state* variable if needed.
    //   *set_* functions should never be passed as props or context

    //   please stick to this naming & usage convention for ease of readability and development

    // <Route path="/home_sister/dashboard" element={<DashRouter />} />
    //                 <Route path="/home_sister/dashboard/account" element={<ActMan />} />
    //                 <Route path="/home_sister/dashboard/scenarios" element={<Scenarios />} />
    //                 <Route path="/home_sister/dashboard/notifications" element={<Notification />} />
    //                 <Route path="/home_sister/dashboard/ssh" element={<SshConnect_temp />} />
    //                 <Route path="/home_sister/devtable" element={<DevTable />} />


       {/* <Route path="/home_sister/dashboard/scenarios/*" element={<Scenarios />} />
                    <Route path="/home_sister/dashboard/account/*" element={<Accountmgmt />} />
                    <Route path="/home_sister/dashboard/notifications" element={<Notification />} />
                    <Route path="/home_sister/dashboard/ssh" element={<SSHconnect />} />
                    <Route path="/home_sister/dashboard/devtable" element={<DevTable />} />
                    <Route path="/home_sister/dashboard/admin/*" element={<AdminDash />} />
                    <Route path="/home_sister/dashboard/instructor/*" element={<InstructorDash />} /> */}