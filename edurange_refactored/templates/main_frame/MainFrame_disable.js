// "use strict";

// import React, { useState, useEffect} from 'react';
// import { Route, Routes } from 'react-router-dom';
// import { Auth_ContextProvider } from './Auth_ContextProvider';
// import OptionsMenu from '../options/OptionsMenu';
// import Login from './components/login/Login';
// import FrameHead from './components/head/FrameHead';
// import Logout_temp from './components/temp/Logout_temp';
// import DashRouter from '../newDash/components/main/DashRouter';
// import EduRangeHome from './components/home/EduRangeHome';
// import InfoRouter from '../info/main/InfoRouter';
// import FrameFoot from './components/foot/FrameFoot';

// import '../../../assets/css/pucs.css'; // - Project Unified Custom Styles (pucs.css) cancels out and effectively replaces the original 'styles.css' from the legacy UI
// import './MainFrame.css'; // styling specific to the mainframe component.  It is important that component-specific styling like this come AFTER the 'pucs.css' import.

// export const MainFrameContext = React.createContext();
// function MainFrame() {
  
//   const connectIP = "127.0.0.1";
//   const connectPort = "8008"; // or whatever your normal port is
//   const loginRoute = "/edurange3/login"
  
//   ////HOOKS//////////////////////////////////////
//     const [ session_csrfToken_state,       set_session_csrfToken_state]       = useState(null);
//     const [ session_userData_state,        set_session_userData_state]        = useState({});
//     const [ session_instructorData_state,  set_session_instructorData_state]  = useState({});
    
//     const [ login_state,                   set_login_state]                   = useState(() => {
//       const edurange_session_String = sessionStorage.getItem('edurange_session');
  
//       if (!edurange_session_String) return false;  // if no session data is found
//       console.log ("user session string: ",edurange_session_String)
//       const edurange_session = JSON.parse(edurange_session_String);
//       const isLoggedIn = edurange_session.logged_in;
//       const expiry = edurange_session.expiry;
  
//       if (isLoggedIn && Date.now() < expiry) {
//           return true;
//       }
//       else { return false; };
//     });
// ///////////////////////////////////////////////

// // Will get initial CSRF token upon page load 
// useEffect(() => {
//   async function fetch_csrfToken () {
//     try {
//       const embedded_csrf = document.querySelector('meta[name="edurange3_csrf"]');
//       if (embedded_csrf) { set_session_csrfToken_state (embedded_csrf.content); }
//     } catch (error) {
//       console.error('Unable to fetch CSRF token.', error);
//     }

//   };
//   fetch_csrfToken();
// }, [  ]);

// useEffect(() => {
//   const currentURL = location.pathname;
//   sessionStorage.setItem('currentURL', currentURL);
// }, [location]);

// return (
//     <div id='edurange-appframe'>

//       <MainFrameContext.Provider value={{

//                 connectIP, connectPort, loginRoute,

//                 session_csrfToken_state,      set_session_csrfToken_state,
//                 session_userData_state,       set_session_userData_state,
//                 session_instructorData_state, set_session_instructorData_state,
//                 login_state,                  set_login_state

//             }}>
              
//           <FrameHead />
//           <div id='edurange-content'>
//             <div className='universal-content-outer'>
//               <div className='universal-content-mid'>
//                 <div className='universal-content-inner'>
//                   <Routes>
//                     <Route path="/edurange3/" element={<EduRangeHome />} />
//                     <Route path="/edurange3/login" element={<Login />} />
//                     <Route path="/edurange3/logout" element={<Logout_temp />} />
//                     <Route path="/edurange3/options" element={<OptionsMenu />} />
//                     <Route path="/edurange3/info/*" element={<InfoRouter />} />
//                       <Route path="/edurange3/dashboard/*" element={
//                         <Auth_ContextProvider>
//                           <DashRouter />
//                         </Auth_ContextProvider>
//                       } />
//                   </Routes>
//                 </div>
//               </div>
//             </div>
//           </div>
//         <FrameFoot />
//       </MainFrameContext.Provider>
//     </div>
//   );
// }

// export default MainFrame;
