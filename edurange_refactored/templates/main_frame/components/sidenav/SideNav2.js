
"use strict";
import React, { useContext } from 'react';
import { MainFrameContext } from '../../MainFrame';
import hamburger from '../../../../static/build/img/hamburger.png';
import { NavData } from './NavData';


import './SideNav2.css'

function SideNav2 () {

return (

    <div className='exo-sidenav-frame'>
        <div className="exo-sidenav-body">
            <div className='exo-sidenav-menu'>

                <ul>

                {NavData.map((val,key) => {
                    // replace link w/ tab state change
                    return (
                        <li key={key} onClick={()=> {window.location.pathname = val.link}}> 
                            <div>{val.icon}</div>
                            <div>{val.title}</div>
                            <div>{val.link}</div>
                        </li>
                    )
                    
                })}
                </ul>
            </div>    
        </div>
    </div>
)    

} export default SideNav2;