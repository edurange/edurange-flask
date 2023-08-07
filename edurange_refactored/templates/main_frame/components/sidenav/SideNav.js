
"use strict";
import React, { useContext } from 'react';
import { MainFrameContext } from '../../MainFrame';
import { SideNav_admin_logged_in, SideNav_instructor_logged_in, SideNav_student_logged_in, SideNav_logged_out } from '../../../../scripts/routing/NavData';

import { Link } from 'react-router-dom';

import './../../MainFrame.css'
import './SideNav.css'

function SideNav () {

    const   {   activeTab_state,  update_tabChoice_status,
                login_state 
            } = useContext(MainFrameContext);

    const navDataToShow = login_state === 1 ? SideNav_admin_logged_in : SideNav_logged_out; // needs update for permissions!  ***************

    return (

        <div className='exo-sidenav-frame'>
            <div className="exo-sidenav-body">
                <div className='exo-sidenav-menu'>
                    <ul className='exo-sidenav-list'>
                        {navDataToShow.map((val,key) => {
                            return (
                                <Link to={val.path} key={key}>
                                <li className='exo-sidenav-row'>
                                        <div id='exo-sidenav-icon'>{val.icon}</div>
                                        <div id='exo-sidenav-title'>{val.title}</div>
                                    </li>
                                </Link>
                            );
                        })}
                    </ul>
                </div>    
            </div>
        </div>
    );

}; export default SideNav;