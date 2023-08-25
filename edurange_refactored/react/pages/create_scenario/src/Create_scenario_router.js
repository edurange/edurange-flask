"use strict";

import React, { useState, useEffect} from 'react';
import { Route, Routes, useNavigate } from 'react-router-dom';

import '../../../assets/css/unified/pucs.css';
import './CreateScenario.css'; 
import CreateScenario from './CreateScenario';
import { LoggedIn_context } from '../../../modules/context/LoggedIn_context';

            import Dashboard_router from '../dashboard/src/Dashboard_router';
//import OptionsMenu from '../options/src/OptionsMenu';
//import InfoRouter from '../info/src/Info_router';

export const CreateScenarioRouterContext = React.createContext();
function CreateScenario_router() {
  
  const connectIP = "127.0.0.1";
  const connectPort = "8008"; // or whatever your normal port is
  const loginRoute = "/edurange3/login"
  
  const navigate = useNavigate();
////HOOKS//////////////////////////////////////
    
  const [ csrfToken_state,        set_csrfToken_state]        = useState(null);
  const [ userData_state,         set_userData_state]         = useState({});
  const [ instructorData_state,   set_instructorData_state]   = useState({});    
    
  // this big ugly mess restores non-secure session info like page URL and 'logged in'
  const [ login_state,            set_login_state]            = useState(() => {
    const edurange3_session_string = sessionStorage.getItem('edurange3_session');
    if (!edurange3_session_string) return false;  // if no session data is found
    console.log ("user session string: ",edurange3_session_string)
    const edurange3_session = JSON.parse(edurange3_session_string);
    const isLoggedIn = edurange3_session.isLoggedIn;
    const expiry = edurange3_session.expiry;
    const returnURL = edurange3_session.currentURL;
    if (returnURL) {navigate(returnURL);};
    if (isLoggedIn && Date.now() < expiry) { return true; }
    else { return false; };
  });

///////////////////////////////////////////////

// Will get initial CSRF token upon page load 
useEffect(() => {
  async function fetch_csrfToken () {
    try {
      const embedded_csrf = document.querySelector('meta[name="edurange3_csrf"]');
      if (embedded_csrf) {
        console.log("csrf received:", embedded_csrf.content)
        set_csrfToken_state (embedded_csrf.content); }
    } catch (error) { console.error('Unable to fetch CSRF token.', error); }
  };
  fetch_csrfToken();
}, []);
// Saves current URL to sessionStorage on navigate for refresh persistence
useEffect(() => {
  const currentURL = location.pathname;
  sessionStorage.setItem('currentURL', currentURL);
}, [location]);

return (
    <div id='edurange-appframe'>

      <CreateScenarioRouterContext.Provider value={{

                connectIP, 
                connectPort, 
                loginRoute,
                csrfToken_state,      set_csrfToken_state,
                userData_state,       set_userData_state,
                login_state,          set_login_state,

                instructorData_state, set_instructorData_state,

            }}>
              
          <CreateScenarioHead />
          <div id='edurange-content'>
            <div className='universal-content-outer'>
              <div className='universal-content-mid'>
                <div className='universal-content-inner'>
                  <Routes>
                    <Route path="/edurange3/" element={<CreateScenario />} />
                    <Route path="/edurange3/login" element={<Login3 />} />
                    <Route path="/edurange3/logout" element={<Logout />} />
                    <Route path="/edurange3/options" element={<OptionsMenu />} />
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
        <CreateScenarioFoot />
      </CreateScenarioRouterContext.Provider>
    </div>
  );
}

export default CreateScenario_router;
