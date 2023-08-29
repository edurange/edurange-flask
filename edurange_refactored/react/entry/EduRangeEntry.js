

///////////////////////
////// EduRangeEntry.js is the primary Main Entry script for EduRange-React
////// Acts more or less as an App.js would in normal React contexts
////// Should be kept as clean as possible
///////////////////////

// Home_router.js is the secondary main entry point Component.

import AxiosConfig from '../api/config/AxiosConfig';
import React from 'react';
import ReactDOM from "react-dom/client";
import { BrowserRouter } from 'react-router-dom';
import Home_router from '../pages/home/src/Home_router';
import '../assets/css/unified/pucs.css' 
// Importing pucs.css here adds pucs.css to full project's bundle.
// That means there's no need to import it separately into your components.

const root = ReactDOM.createRoot(document.getElementById("edurange3_entry_id"));
root.render (
    // <React.StrictMode>
            <AxiosConfig>
                <BrowserRouter>
                    <Home_router/>
                </BrowserRouter>
            </AxiosConfig>
    // </React.StrictMode>
);