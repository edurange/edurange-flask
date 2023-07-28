import {createRoot} from 'react-dom/client';
import React, { useState, useEffect } from 'react';
import ChildComponent2 from './ChildComponent2';
import ChildComponent3 from './ChildComponent3';
import ChildComponent4 from './ChildComponent4';
import ChildComponent5 from './ChildComponent5';
import ChildComponent6 from './ChildComponent6';
import LoginFromNav from './components/login_from_nav/LoginFromNav';
import Welcome from '../welcome_page/components/main/Welcome';
import './MainFrame.css';
// import '../../../node_modules/bootstrap/dist/css/bootstrap.css'

function MainFrame() {
    const [activeTab, setActiveTab] = useState(1);
    const [desiredTab, setDesiredTab] = useState(1);
    useEffect(() =>  {setActiveTab(desiredTab);}, [desiredTab]); 
    // const MainFrameContext = React.createContext();

    return (
        <div id='master'>
                {/* <MainFrameContext.Provider value={{ activeTab, setDesiredTab }}> */}
                <div id='master-tabs'>
                    <div uid={0} onClick={() => setDesiredTab(1)} className={activeTab === 1 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>INTRO</div></div>
                    <div uid={1} onClick={() => setDesiredTab(2)} className={activeTab === 2 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>MISSION</div></div>
                    <div uid={2} onClick={() => setDesiredTab(3)} className={activeTab === 3 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>STUDENTS</div></div>
                    <div uid={3} onClick={() => setDesiredTab(4)} className={activeTab === 4 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>TEACHERS</div></div>
                    <div uid={4} onClick={() => setDesiredTab(5)} className={activeTab === 5 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>DOCS / HELP</div></div>
                    <div uid={5} onClick={() => setDesiredTab(6)} className={activeTab === 6 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>OPTIONS</div></div>
                    <div uid={6} onClick={() => setDesiredTab(7)} className={activeTab === 7 ? "tabs active-tab" : "tabs inactive-tab"}><div className='tab-label'>LOGIN</div></div>
                </div>

                <section className={activeTab === 1 ? "active-page universal-page-container" : "hide"}> <Welcome/></section>
                <section className={activeTab === 2 ? "active-page universal-page-container" : "hide"}> <ChildComponent2/></section>
                <section className={activeTab === 3 ? "active-page universal-page-container" : "hide"}> <ChildComponent3/></section>
                <section className={activeTab === 4 ? "active-page universal-page-container" : "hide"}> <ChildComponent4/></section>
                <section className={activeTab === 5 ? "active-page universal-page-container" : "hide"}> <ChildComponent5/></section>
                <section className={activeTab === 6 ? "active-page universal-page-container" : "hide"}> <ChildComponent6/></section>
                <section className={activeTab === 7 ? "active-page universal-page-container" : "hide"}> <LoginFromNav/></section>
                {/* </MainFrameContext.Provider> */}
            </div>
    );
}

const entryPoint = document.getElementById('react-entry-id');
const root=createRoot(entryPoint);
root.render(<MainFrame/>);
