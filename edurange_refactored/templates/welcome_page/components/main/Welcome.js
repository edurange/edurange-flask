
import './Welcome.css';
import MainFrame from '../../../main_frame/MainFrame';


import {createRoot} from 'react-dom/client';
import React, { useState, useEffect } from 'react';

function Welcome(props) {
    return (
        <div>
            <MainFrame>
                <br></br>
                Welcome.js Rendered.
                <h2>Welcome to EDURange.</h2>
                <p> Yada yada yada yada yada yada yada </p> <br></br>
                <p> Yada yada yada yada yada yada yada </p> <br></br>
                <p> Yada yada yada yada yada yada yada </p> <br></br>
                <p> Yada yada yada yada yada yada yada </p> <br></br>
                <p> Yada yada yada yada yada yada yada </p> <br></br>
                <p> Yada yada yada yada yada yada yada </p> <br></br>
                
            </MainFrame>
        </div>
    );
}

export default Welcome;

var e = document.getElementById('welcome-page'); // The id assigned in html file. 
const root=createRoot(e);

root.render(<Welcome/>);






