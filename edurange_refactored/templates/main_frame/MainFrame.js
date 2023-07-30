"use strict";

import {createRoot} from 'react-dom/client';
import React, { useState, useEffect} from 'react';

import Welcome from './Welcome';
import DashBoard_sister from './DashBoard_sister';
import Scenarios_sister from './Scenarios_sister';
import Notification from '../notification_history/components/Notification';
import Documents from './Documents';
import OptionsMenu from './OptionsMenu';
import LoginFromNav from './components/login_from_nav/LoginFromNav';
import FrameHead from './components/head/FrameHead';
import FrameFoot from './components/foot/FrameFoot';


import './MainFrame.css';
import SideNav2 from './components/sidenav/SideNav2';

export const MainFrameContext = React.createContext();

function MainFrame() {

    const connectIP = "127.0.0.1";
    const connectPort = "8008";
    const loginRoute = "/home_sister/"

////HOOKS//////////////////////////////////////
    const [activeTab_state, set_activeTab_state] = useState(1);
    const [new_tabChoice_status, update_tabChoice_status] = useState(1);

    const [csrfToken_state, set_csrfToken_state] = useState(null);
    const [new_csrfToken_status, update_csrfToken_status] = useState(null);

    const [login_state, set_login_state] = useState(0);
    const [new_login_status, update_login_status] = useState(0);

    useEffect(() =>  {set_activeTab_state(new_tabChoice_status);}, [new_tabChoice_status]); 
    useEffect(() =>  {set_csrfToken_state(new_csrfToken_status);}, [new_csrfToken_status]); 
    useEffect(() =>  {set_login_state(new_login_status);}, [new_login_status]); 
///////////////////////////////////////////////

    // const conditionalRender = (() => { return login_state === 0 ? <LoginFromNav/> : <Welcome/>; })();

    return (
        <div id='edurange-appframe'>
    
            <MainFrameContext.Provider value={{
                activeTab_state,    update_tabChoice_status,
                login_state,        update_login_status,
                csrfToken_state,    update_csrfToken_status,
                connectIP, connectPort, loginRoute
            }}>

                <FrameHead/>
                <div id='edurange-content'>
                    <SideNav2/>
                    <div className='universal-content-outer'>
                        <div className='universal-content-mid'>
                            <section className={activeTab_state === 1 ? "active-page" : "hide"}> <Welcome/></section>
                            <section className={activeTab_state === 2 ? "active-page" : "hide"}> <DashBoard_sister/></section>
                            <section className={activeTab_state === 3 ? "active-page" : "hide"}> <Scenarios_sister/></section>
                            <section className={activeTab_state === 4 ? "active-page" : "hide"}> <Notification/></section>
                            <section className={activeTab_state === 5 ? "active-page" : "hide"}> <SideNav2/></section>
                            <section className={activeTab_state === 6 ? "active-page" : "hide"}> <OptionsMenu/></section>
                            <section className={activeTab_state === 7 ? "active-page" : "hide"}> <LoginFromNav/></section>
                        </div>
                    </div>
                </div>
                <FrameFoot/>

            </MainFrameContext.Provider>

        </div>
    );
}

export default MainFrame;
const entryPoint = document.getElementById('react-entry-id');
const root=createRoot(entryPoint);
root.render(<MainFrame/>);

    // The state hooks in this component are paired so one can act as a trigger for the other w/ useEffect
    // which can help prevent some render problems and allow for increased flexibility in how to handle
    // implementation of useEffect-triggered functions, while reducing confusion as to whether a state-setter
    // is actually changing state or calling a function.  a naming convention will help clarify.

    // Convention and state update flow: 
    //   - The *_state* variables are the main states, and their *set_* partners are ***useEffect only***
    //   - The *update_* function calls are used to update the *_status* variables
    //   - When a *_status* variable changes, that triggers a useEffect update from context provider component
    //   - This matching useEffect update then calls the actual *set_* function using the *_status* value as an argument.
    //   - The *set_* function then finally updates the original *_state* variable to match the *_status* variable / arg.
    //
    //   To change state in normal calls, the *update_* function should be used, not the *set_*
    //   which means that when passing down a 'setter' type function, always pass the *update_* version, 
    //   as well as the original *_state* variable if needed.
    //   *set_* functions should never be passed as props or context

    //   please stick to this naming & usage convention for ease of readability and development
