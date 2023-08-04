"use strict";

import {createRoot} from 'react-dom/client';
import React, { useState, useEffect} from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';


// ultimately a better import system might be needed but this is okay for now.
import Welcome_temp from './components/temp/Welcome_temp';
import DashBoard_temp from './components/temp/Dashboard_temp'
import Scenarios_temp from './components/temp/Scenarios_temp';
import Notification from '../notification_history/components/Notification';
import Documents_temp from './components/temp/Documents_temp';
import Options_temp from './components/temp/Options_temp';
import LoginFromNav from './components/login_from_nav/LoginFromNav';
import FrameHead from './components/head/FrameHead';
import FrameFoot from './components/foot/FrameFoot';
import Logout_temp from './components/temp/Logout_temp';
import Admin_temp from './components/temp/Admin_temp';
import Instructor_temp from './components/temp/Instructor_temp';
import About_temp from './components/temp/About_temp';
import Contact_temp from './components/temp/Contact_temp';
import Account_temp from './components/temp/Account_temp';
import SideNav from './components/sidenav/SideNav';

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
                connectIP, connectPort, loginRoute
            }}>
        <FrameHead />
        <Router>
          <div id='edurange-content'>
            <SideNav testData='test_1' />
            <div className='universal-content-outer'>
              <div className='universal-content-mid'>
                <Routes>
                  <Route path="/home_sister/" element={<Welcome_temp />} />
                  <Route path="/home_sister/login" element={<LoginFromNav />} />
                  <Route path="/home_sister/logout" element={<Logout_temp />} />
                  <Route path="/home_sister/options" element={<Options_temp />} />
                  <Route path="/home_sister/admin" element={<Admin_temp />} />
                  <Route path="/home_sister/instructor" element={<Instructor_temp />} />
                  <Route path="/home_sister/info/" element={<About_temp />} />
                  <Route path="/home_sister/info/about" element={<About_temp />} />
                  <Route path="/home_sister/info/docs" element={<Documents_temp />} />
                  <Route path="/home_sister/info/contact" element={<Contact_temp />} />
                  <Route path="/home_sister/dashboard" element={<DashBoard_temp />} />
                  <Route path="/home_sister/dashboard/account" element={<Account_temp />} />
                  <Route path="/home_sister/dashboard/scenarios" element={<Scenarios_temp />} />
                  <Route path="/home_sister/dashboard/notifications" element={<Notification />} />
                </Routes>
              </div>
            </div>
          </div>
        </Router>
        <FrameFoot />
      </MainFrameContext.Provider>
    </div>
  );
}

export default MainFrame;
const entryPoint = document.getElementById('react-entry-id');
const root=createRoot(entryPoint);
root.render(<MainFrame/>);

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
