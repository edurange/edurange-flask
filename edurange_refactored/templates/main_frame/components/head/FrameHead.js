"use strict";
import React, { useContext } from 'react';
import { MainFrameContext } from '../../MainFrame';
import hamburger from '../../../../static/build/img/hamburger.png';
import './FrameHead.css';
import { FaBell } from "react-icons/fa6";
import SideNav from '../sidenav/SideNav';

const FrameHead = () => {
  
////HOOKS//////////////////////////////////////
//  hook declarations:
//  imported props:
    const { activeTab_state,  update_tabChoice_status } = useContext(MainFrameContext);
//////////////////////////////////////////////

    const toggle_sideNav = () => {
        const sidebar = document.querySelector('.exo-sidenav-frame');
        sidebar.classList.toggle('show_sidenav');
    };
    
    return (
        <div id='edurange-navhead'>
            <div className='exo-hamburger-outer' onClick={toggle_sideNav}>
                <div className='exo-hamburger-inner'>
                    <img src={hamburger} alt="[X]"/>
                </div>
            </div>
            <div uid={0} onClick={() => update_tabChoice_status(1)} className={activeTab_state === 1 ? "exo-nav-tabs exo-nav-active-tab" : "exo-nav-tabs exo-nav-inactive-tab"}><div className='exo-nav-tab-label'>HOME</div></div>
            <div uid={1} onClick={() => update_tabChoice_status(2)} className={activeTab_state === 2 ? "exo-nav-tabs exo-nav-active-tab" : "exo-nav-tabs exo-nav-inactive-tab"}><div className='exo-nav-tab-label'>DASHBOARD</div></div>
            <div uid={2} onClick={() => update_tabChoice_status(3)} className={activeTab_state === 3 ? "exo-nav-tabs exo-nav-active-tab" : "exo-nav-tabs exo-nav-inactive-tab"}><div className='exo-nav-tab-label'>SCENARIOS</div></div>
            <div uid={3} onClick={() => update_tabChoice_status(4)} className={activeTab_state === 4 ? "exo-nav-tabs exo-nav-active-tab" : "exo-nav-tabs exo-nav-inactive-tab"}><div className='exo-nav-tab-label'>NOTIFICATIONS</div></div>
            <div uid={4} onClick={() => update_tabChoice_status(5)} className={activeTab_state === 5 ? "exo-nav-tabs exo-nav-active-tab" : "exo-nav-tabs exo-nav-inactive-tab"}><div className='exo-nav-tab-label'>DOCS</div></div>
            <div uid={5} onClick={() => update_tabChoice_status(6)} className={activeTab_state === 6 ? "exo-nav-tabs exo-nav-active-tab" : "exo-nav-tabs exo-nav-inactive-tab"}><div className='exo-nav-tab-label'>OPTIONS</div></div>
            <div uid={6} onClick={() => update_tabChoice_status(7)} className={activeTab_state === 7 ? "exo-nav-tabs exo-nav-active-tab" : "exo-nav-tabs exo-nav-inactive-tab"}><div className='exo-nav-tab-label'>LOGIN</div></div>
        </div>
    );
}
export default FrameHead;
