
"use strict";
import React, { useContext } from 'react';
import { MainFrameContext } from '../../MainFrame';
import { NavData_logged_in, NavData_logged_out } from './NavData';
import { Link } from 'react-router-dom';

import './../../MainFrame.css'

function SideNav () {

    const   {   activeTab_state,  update_tabChoice_status,
                login_state 
            } = useContext(MainFrameContext);

    const navDataToShow = login_state === 1 ? NavData_logged_in : NavData_logged_out;

    return (

        <div className='exo-sidenav-frame'>
            <div className="exo-sidenav-body">
                <div className='exo-sidenav-menu'>
                    <ul className='exo-sidenav-list'>
                        {navDataToShow.map((val,key) => {
                            return (
                                // <li key={key} className='exo-sidenav-row' onClick={()=> {update_tabChoice_status(val.link)}}> 
                                //     <div id='exo-sidenav-icon'>{val.icon}</div>
                                //     <div id='exo-sidenav-title'>{val.title}</div>
                                // </li>
                                <Link to={val.path} key={key}> {/* Use the Link component here */}
                                    <li className='exo-sidenav-row' onClick={() => { update_tabChoice_status(val.link) }}>
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