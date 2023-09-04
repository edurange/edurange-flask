import React, {useContext} from 'react';
import { navArrays } from '../../../../../modules/nav/navItemsData';
import '../Dashboard.css';
import { nanoid } from 'nanoid';
import { HomeRouterContext } from '../../../src/Home_router';

function DashSidebar({navToShow}) {

  const { updateNav } = useContext(HomeRouterContext);
  
  navToShow = (navToShow) ? navToShow : navArrays.side_logout; 
    
  return (
        <div className='newdash-sidebar-frame'>
          {navToShow.map((val, key) => {
            return (
              <div className='edu3-nav-link' key={nanoid(3)} onClick={() => updateNav(val.path, val.navStub)} >
                <li className='newdash-sidebar-row'>
                  <div id='newdash-sidebar-icon'>{val.icon}</div>
                  <div id='newdash-sidebar-title'>{val.title}</div>
                </li>
              </div>
            );
          })}
        </div>
  );
};
export default DashSidebar;
