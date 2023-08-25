
import React from 'react';
import { Link } from 'react-router-dom';
import '../Dashboard.css';

function DashSidebar(props) {
  
  return (
        <div className='newdash-sidebar-frame'>
          {props.navDataToShow.map((val, key) => {
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
}

export default DashSidebar;
