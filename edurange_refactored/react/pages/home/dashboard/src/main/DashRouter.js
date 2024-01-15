// import React, { useContext } from 'react';
// import './NewDash.css';
// import { MainFrameContext } from '../../../main_frame/MainFrame';
// import { Link, Route, Routes } from 'react-router-dom';
// import Scenarios from '../scenarios/Scenarios';
// import '../../../../modules/ui/navItemsData'
// import {
//   DashSideNav_logged_out,
//   DashSideNav_student_logged_in,
//   DashSideNav_instructor_logged_in,
//   DashSideNav_admin_logged_in,
// } from '../../../../modules/ui/navItemsData';
// import InstructorDash from '../instructor/InstructorDash';
// import Admin_home from '../admin/Admin_home';
// import DashHome from '../Dashboard_home';
// import SSHmodal from '../ssh/SSHmodal';
// import Users from '../users/Users';
// import UserGroups from '../users/UserGroups';
// import ScenarioGroups from '../scenarios/ScenarioGroups';
// import DashNotifications from '../notifications/components/DashNotifications';
// import Account from '../account/Account';
// import ScenarioCardDetail from '../scenarios/ScenarioCardDetail';
// import ScenarioFullView from '../scenarios/ScenarioFullView';
// import JWTAUTH from '../components/JWTAUTH';
// import Accountmgmt from '../../../accountmgmt/components/main/Accountmgmt';

// function DashRouter() {

//   const { 
//     login_state, 
//     session_userData_state,
//   } = useContext(MainFrameContext);

//   const dataType = Object.freeze({
//     USERS: 0,
//     USER_GROUPS: 1,
//     SCENARIOS: 2,
//     SCENARIO_GROUPS: 3
//   });
//   console.log("user is logged in: ",login_state)
//   const navDataToShow = login_state === true ? DashSideNav_admin_logged_in : DashSideNav_logged_out; // needs update for permissions!  ***************
//   return (

//     <div className='newdash-frame'>
//       <div className='newdash-frame-carpet'>

//         <div className='newdash-sidebar-frame'>
//           {navDataToShow.map((val, key) => {
//             return (
//               <Link to={val.path} key={key}>
//                 <li className='newdash-sidebar-row'>
//                   <div id='newdash-sidebar-icon'>{val.icon}</div>
//                   <div id='newdash-sidebar-title'>{val.title}</div>
//                 </li>
//               </Link>
//             );
//           })}

//         </div>

//         <div className="newdash-infopane-frame">
//           <div className='newdash-infopane-content'>
//             <Routes>
//               <Route path="/*" element={<DashHome />} />
//               <Route path="/admin/*" element={<Admin_home />} />
//               <Route path="/instructor/*" element={<InstructorDash />} />
//               <Route path="/account" element={<Accountmgmt />} />
//               <Route path="/users" element={<Users />} />
//               <Route path="/userGroups" element={<UserGroups />} />
//               <Route path="/scenarios" element={<Scenarios />} />
//               <Route path="/scenarios/:uid/:pageID" element={<ScenarioFullView />}/>
//               <Route path="/scenarioGroups" element={<ScenarioGroups />} />
//               <Route path="/notifications" element={<DashNotifications />} />
//               <Route path="/ssh" element={<SSHmodal />} />
//               <Route path="/jwt_auth" element={<JWTAUTH  />} />
//             </Routes>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default DashRouter;
