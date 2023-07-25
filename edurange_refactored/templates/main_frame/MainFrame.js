import  './../../../assets/css/pucs';
import  './../../../assets/css/style';
import 'bootstrap/dist/css/bootstrap.css';
import './MainFrame.css';
import React, {useState, useEffect} from 'react';

function MainFrame({ children }) {

    return (

        <div className='blargenstein'>

                <div>
                    MainFrame.js rendered
                    {children}
                </div>
        </div>
    );
}

export default MainFrame;
