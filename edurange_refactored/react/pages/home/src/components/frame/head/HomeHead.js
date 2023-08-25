"use strict";
import React, { useContext } from 'react';
import './HomeHead.css';
import { Link } from 'react-router-dom';
import { HomeRouterContext } from '../../../Home_router';
import { 
    TopNav_admin_logged_in,
    TopNav_instructor_logged_in, 
    TopNav_student_logged_in, 
    TopNav_logged_out } 
    from '../../../../../../modules/nav/navItemsData';

function HomeHead () {
  
    const { login_state } = useContext(HomeRouterContext);

    const navDataToShow = login_state === true ? TopNav_admin_logged_in : TopNav_logged_out; 
    
    return (
        <div id='edurange-navhead'>
            <span id="edurange-navhead-buttonbar">

            {navDataToShow.map((val,key) => {
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