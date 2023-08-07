"use strict";
import React, { useContext } from 'react';
import { MainFrameContext } from '../../MainFrame';
import './FrameHead.css';
import { FaBell } from "react-icons/fa6";
import { edurange_icons } from "../../edurange_icons";
import { TopNav_admin_logged_in, TopNav_instructor_logged_in, TopNav_student_logged_in, TopNav_logged_out } from '../../../../scripts/routing/NavData'


import { Link } from 'react-router-dom';

const FrameHead = () => {
  


    
    //HOOKS//////////////////////////////////////
    //  hook declarations:
    //  imported props:
    const { login_state, activeTab_state,  update_tabChoice_status } = useContext(MainFrameContext);
    ////////////////////////////////////////////
    const navDataToShow = login_state === 1 ? TopNav_admin_logged_in : TopNav_logged_out; 

    const toggle_sideNav = () => {
        const sidebar = document.querySelector('.exo-sidenav-frame');
        sidebar.classList.toggle('show_sidenav');
    };
    
    return (
        <div id='edurange-navhead'>
            <div className='exo-hamburger-outer' onClick={toggle_sideNav}>
                <div className='exo-hamburger-inner'>
                    {edurange_icons.hamburger_icon}
                    {/* X */}
                </div>
            </div>
            <span id="edurange-navhead-buttonbar">

            {navDataToShow.map((val,key) => {
                return (
                    <Link to={val.path} key={key}>
                        <li className='topnav-button-panes' onClick={() => { update_tabChoice_status(val.link) }}>
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
export default FrameHead;