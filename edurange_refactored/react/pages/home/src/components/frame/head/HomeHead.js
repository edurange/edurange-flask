"use strict";
import React, { useContext } from 'react';
import { nanoid } from 'nanoid';
import { HomeRouterContext } from '../../../Home_router';
import edurange_icons from '../../../../../../modules/ui/edurangeIcons';
import Notifs_button from './Notifs_button';
import './HomeHead.css';

function HomeHead({ navToShow }) {

    const {
        updateNav, navName_state,
        sideNav_isVisible_state, set_sideNav_isVisible_state,
        sideNav_isSmall_state, set_sideNav_isSmall_state
    } = useContext(HomeRouterContext);

    function toggle_sideNav_vis() {
        set_sideNav_isVisible_state(!sideNav_isVisible_state); // toggle to opposite
    };
    function toggle_sideNav_size(){
        set_sideNav_isSmall_state(!sideNav_isSmall_state); // toggle to opposite
    };
    function chooseSideIcon () {
        if (sideNav_isVisible_state){
            return (<>

                <div 
                    className='er3-homehead-hamburger-item hamburger-jr hamburger-pill-right' 
                    onClick={() => toggle_sideNav_size()} 
                >
                {(sideNav_isSmall_state) ? edurange_icons.panelOpen_left : edurange_icons.panelClose_left}
                    </div>
                </>
            )
        }
        else return (<></>);
    };

    const panelVisSelector = (sideNav_isVisible_state) ? edurange_icons.menuClose_up : edurange_icons.menuOpen_down;
    const panelSizeSelector = chooseSideIcon();
    const pillOrReg = (sideNav_isVisible_state) ? 'er3-homehead-hamburger-item hamburger-pill-left' : 'er3-homehead-hamburger-item';

    function Hamburger() {
        if (navName_state === "home" || navName_state === "logout") { return <></> };
        return (
            <div className='er3-homehead-hamburger-frame'>
                <div
                    className={pillOrReg}
                    onClick={() => toggle_sideNav_vis()}
                > {panelVisSelector} </div>

                {panelSizeSelector}

            </div>
            
        );
    };

    return (
        <div className="er3-homehead">

            <div className="er3-homehead-left"><Hamburger /></div>
            <div className='homehead-notifs-section'><Notifs_button/></div>

            <div className='er3-homehead-right'>
                <span className="er3-homehead-buttonbar">
                    {navToShow.map((val, key) => {
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

        </div>
    );
};
export default HomeHead;