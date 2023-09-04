"use strict";
import React, {useContext} from 'react';
import './HomeHead.css';
import '../../../Home.css';
import { navArrays } from '../../../../../../modules/nav/navItemsData';
import { nanoid } from 'nanoid';
import { HomeRouterContext } from '../../../Home_router';

function HomeHead ({navToShow}) {

    const { updateNav } = useContext(HomeRouterContext);
  
    navToShow = (navToShow) ? navToShow : navArrays.top_logout; 
    return (
        <div id='edurange-navhead'>
            <span id="edurange-navhead-buttonbar">

            {navToShow.map((val,key) => {
                return (
                    <div className='edu3-nav-link' key={nanoid(3)} onClick={() => updateNav(val.path, val.navStub)} >
                        <li className='topnav-button-panes' >
                            <div className='topnav-icon-box' >{val.icon}</div>
                            <div className='topnav-label-box' >{val.title}</div>
                        </li>
                    </div>
                    );
                })}
            </span>
        </div>
    );
}
export default HomeHead;