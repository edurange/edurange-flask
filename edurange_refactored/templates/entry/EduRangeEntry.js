
import React from 'react';
import ReactDOM from "react-dom/client";
import MainFrame from '../main_frame/MainFrame';

import { BrowserRouter } from 'react-router-dom';

const root = ReactDOM.createRoot(document.getElementById("react-entry-id"));
root.render (
    <React.StrictMode>
        <BrowserRouter>
            <MainFrame/>
        </BrowserRouter>
    </React.StrictMode>
)