
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Contact from '../contact/src/Contact';
import HelpPage from '../help/src/HelpPage';
import InfoHome from './Info_home';
import About from '../about/src/About';
import Documents from '../docs/src/Documents';

function InfoRouter (    ) {

    return (
        <div className='exo-dashpanes-outer-wrap'>
                <div className='dash-sidebar-pane'>
                This is the InfoHome 'wrapper' rendering successfully.
                </div>
                    <div className="exo-dashpanes-container">
                    <div className='exo-dashpane'>
                        <Routes>
                            <Route path="/*" element={<InfoHome />} />
                            <Route path="/help" element={<HelpPage />} />
                            <Route path="/contact" element={<Contact />} />
                            <Route path="/docs" element={<Documents />} />
                            <Route path="/about" element={<About />} />
                        </Routes>
                    </div>            
                </div>
        </div>
    );
}

export default InfoRouter;
