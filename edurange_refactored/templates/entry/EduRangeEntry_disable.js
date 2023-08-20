

///////////////////////
////// EduRangeEntry.js is the primary Main Entry script for EduRange-React
////// Acts more or less as an App.js would in normal React contexts
////// Should be kept as clean as possible
///////////////////////

// MainFrame.js is the secondary main entry point Component.

import React from 'react';
import ReactDOM from "react-dom/client";
import MainFrame from '../main_frame/MainFrame';

import { BrowserRouter } from 'react-router-dom';

const root = ReactDOM.createRoot(document.getElementById("edurange3_entry_id"));
root.render (
    <React.StrictMode>
        <BrowserRouter>
            <MainFrame/>
        </BrowserRouter>
    </React.StrictMode>
);