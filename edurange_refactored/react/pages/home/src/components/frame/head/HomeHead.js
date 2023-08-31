"use strict";
import React from 'react';
import './HomeHead.css';
import { Link } from 'react-router-dom';
import { navArrays } from '../../../../../../modules/nav/navItemsData';

function HomeHead ({navToShow}) {
  
    navToShow = (navToShow) ? navToShow : navArrays.top_logout; 
        
    return (
        <div id='edurange-navhead'>
            <span id="edurange-navhead-buttonbar">

            {navToShow.map((val,key) => {
                return (
                    <Link to={val.path} key={key}>
                        <li className='topnav-button-panes' >
                            <div className='topnav-icon-box' >{val.icon}</div>
                            <div className='topnav-label-box' >{val.title}</div>
                        </li>
                    </Link>
                    );
                })}
            </span>
        </div>
    );
}
export default HomeHead;