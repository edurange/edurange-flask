"use strict";
import {createRoot} from 'react-dom/client';
import React, { useState, useEffect} from 'react';
import ChildComponent2 from './ChildComponent2';
import ChildComponent3 from './ChildComponent3';
import Documents from './Documents';
import Notification from '../notification_history/components/Notification';
import OptionsMenu from './OptionsMenu';
import LoginFromNav from './components/login_from_nav/LoginFromNav';
import Welcome from '../welcome_page/components/main/Welcome';
import './MainFrame.css';


export const MainFrameContext = React.createContext();

function MainFrame() {

    // The states below are paired so one can act as a trigger for the other in useEffect below
    // which can help prevent some render problems

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

    const [activeTab_state, set_activeTab_state] = useState(4);
    const [new_chosenTab_status, update_chosenTab_status] = useState(4);

    const [csrfToken_state, set_csrfToken_state] = useState(null);
    const [new_csrfToken_status, update_csrfToken_status] = useState(null);

    const [login_state, set_login_state] = useState(0);
    const [new_login_status, update_login_status] = useState(0);

    useEffect(() =>  {set_activeTab_state(new_chosenTab_status);}, [new_chosenTab_status]); 
    useEffect(() =>  {set_csrfToken_state(new_csrfToken_status);}, [new_csrfToken_status]); 
    useEffect(() =>  {set_login_state(new_login_status);}, [new_login_status]); 

    function renderLoginOrRedirect () {
        if (login_state === 0) {return <LoginFromNav/>;} 
        else {return <Welcome/>;}
    };
    const conditionalRender = renderLoginOrRedirect();

    return (
        <div id='master'>
    
            <MainFrameContext.Provider value={{
                activeTab_state,    update_chosenTab_status,
                login_state,        update_login_status,
                csrfToken_state,    update_csrfToken_status
            }}>

                <div id='master-tabs'>
                    <div uid={0} onClick={() => update_chosenTab_status(1)} className={activeTab_state === 1 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>HOME</div></div>
                    <div uid={1} onClick={() => update_chosenTab_status(2)} className={activeTab_state === 2 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>DASHBOARD</div></div>
                    <div uid={2} onClick={() => update_chosenTab_status(3)} className={activeTab_state === 3 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>SCENARIOS</div></div>
                    <div uid={3} onClick={() => update_chosenTab_status(4)} className={activeTab_state === 4 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>NOTIFICATIONS</div></div>
                    <div uid={4} onClick={() => update_chosenTab_status(5)} className={activeTab_state === 5 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>DOCS</div></div>
                    <div uid={5} onClick={() => update_chosenTab_status(6)} className={activeTab_state === 6 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>OPTIONS</div></div>
                    <div uid={6} onClick={() => update_chosenTab_status(7)} className={activeTab_state === 7 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>LOGIN</div></div>
                </div>

                <section className={activeTab_state === 1 ? "active-page universal-page-container" : "hide"}> <Welcome/></section>
                <section className={activeTab_state === 2 ? "active-page universal-page-container" : "hide"}> <ChildComponent2/></section>
                <section className={activeTab_state === 3 ? "active-page universal-page-container" : "hide"}> <ChildComponent3/></section>
                <section className={activeTab_state === 4 ? "active-page universal-page-container" : "hide"}> <Notification/></section>
                <section className={activeTab_state === 5 ? "active-page universal-page-container" : "hide"}> <Documents/></section>
                <section className={activeTab_state === 6 ? "active-page universal-page-container" : "hide"}> <OptionsMenu/></section>
                <section className={activeTab_state === 7 ? "active-page universal-page-container" : "hide"}> {conditionalRender}</section>
            </MainFrameContext.Provider>
        </div>
    );
}

export default MainFrame;
const entryPoint = document.getElementById('react-entry-id');
const root=createRoot(entryPoint);
root.render(<MainFrame/>);
