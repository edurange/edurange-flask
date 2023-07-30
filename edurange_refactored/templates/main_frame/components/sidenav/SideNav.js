
"use strict";
import React, { useContext } from 'react';
import { MainFrameContext } from '../../MainFrame';
import hamburger from '../../../../static/build/img/hamburger.png';

function SideNav () {

return (

    <div>
        <div className="exo-sidenav-frame">
            <a href="#" className="exo-dropnav-item">Item1</a>
            <a href="#" className="exo-dropnav-item">Item2</a>
            <a href="#" className="exo-dropnav-item">Item3</a>
            <a href="#" className="exo-dropnav-item">Item4</a>
            <a href="#" className="exo-dropnav-item">Item5</a>
        </div>
    </div>
)    

} export default SideNav;