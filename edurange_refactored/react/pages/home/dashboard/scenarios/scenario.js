Markdown
67 lines
2.5KB
24 hoursTTL
raw

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67

import React, { useContext, useState } from 'react';
import { Link, Route, Routes } from 'react-router-dom';
import { HomeRouterContext } from '../../src/Home_router';
import Dashboard_home from './Dashboard_home';
import DashSidebar from './sidebar/DashSidebar';
import JWT_Test from '../src/components/JWT_test';

import './Dashboard.css';
import Logout from '../../src/components/logout/Logout';
import Scenarios_router from '../scenarios/src/Scenarios_router';
import DashNotifications from './components/notifications/components/DashNotifications';
import InstructorDash from '../instructor/src/InstructorDash';
import Account from '../account/src/Account';
import SSHmodal from './components/ssh/SSHmodal';
import AdminDash from '../admin/src/AdminDash';
// import navItems from '../../../../modules/nav/navItemsData';

export const DashRouterContext = React.createContext();


function Dashboard_router() {

  // console.log(navItems)

  const { 
    login_state, userData_state,
    sideNavData_state, set_sideNavData_state,
    topNavData_state, set_topNavData_state
  } = useContext(HomeRouterContext);
  
  // const userRole = userData_state['role'] ?? 'none'
  // const navDataName = (login_state) ? `DashSideNav_${userRole}_logged_in}`  : DashSideNav_logged_out;
  // const navDataToShow = navItems.Options_SideNav ?? []
  // const navDataToShow = navItems['navDataName'] ?? []

  // these routes extend /edurange3/dashboard
  // e.g. scenarios is URL /edurange3/dashboard/scenarios
  return (
    

    <div className='newdash-frame'>
      <div className='newdash-frame-carpet'>

        <DashSidebar />

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
              <Route path="/notifications" element={<DashNotifications />} />
              <Route path="/ssh" element={<SSHmodal />} />
            </Routes>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard_router;

 
