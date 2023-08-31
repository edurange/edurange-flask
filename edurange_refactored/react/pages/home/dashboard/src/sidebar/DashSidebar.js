import React from 'react';
import { Link } from 'react-router-dom';
import { navArrays } from '../../../../../modules/nav/navItemsData';
import '../Dashboard.css';

function DashSidebar({navToShow}) {
  
  navToShow = (navToShow) ? navToShow : navArrays.side_logout; 
    
  return (
        <div className='newdash-sidebar-frame'>
          {navToShow.map((val, key) => {
            return (
              <Link to={val.path} key={key}>
                <li className='newdash-sidebar-row'>
                  <div id='newdash-sidebar-icon'>{val.icon}</div>
                  <div id='newdash-sidebar-title'>{val.title}</div>
                </li>
              </Link>
            );
          })}
        </div>
  );
};
export default DashSidebar;