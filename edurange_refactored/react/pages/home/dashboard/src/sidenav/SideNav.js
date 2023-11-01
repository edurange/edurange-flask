import React, {useContext} from 'react';
import { navArrays } from '../../../../../modules/nav/navItemsData';
import { nanoid } from 'nanoid';
import { HomeRouterContext } from '../../../src/Home_router';
import './SideNav.css';

function SideNav({navToShow}) {

  const { 
    updateNav,
    sideNav_isVisible_state,
    sideNav_isSmall_state
  } = useContext(HomeRouterContext);

  navToShow = (navToShow) ? navToShow : navArrays.side_logout; 

  if (!sideNav_isVisible_state) {return <></>}
    
  return (
        <div className='newdash-sidebar-frame'>

          {navToShow.map((val, key) => {
            return (
              <div className='newdash-sidebar-row' key={nanoid(3)} onClick={() => updateNav(val.path, val.navStub)} >
                <div className='newdash-sidebar-item'>
                  <div className='newdash-sidebar-icon'>{val.icon}</div>

                  {(sideNav_isSmall_state) ? <></> : (
                    <div className='newdash-sidebar-title'>
                      {(sideNav_isSmall_state) ? <></> : val.title}
                    </div>
                  )}

                </div>
              </div>
            );
          })}
        </div>
  );
};
export default SideNav;
