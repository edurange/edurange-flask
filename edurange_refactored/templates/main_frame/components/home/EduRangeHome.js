"use strict";
import React, { useContext } from 'react';
import { MainFrameContext } from '../../MainFrame';
function EduRangeHome() {
  
  const { session_userInfo_state, session_instructorData_state } = useContext(MainFrameContext);


    return (
        <div className='universal-page-parent'>
            <div className='universal-page-child'>
                <div className='welcome-text'>welcome to<br/> eduRange&gt;<span className='blink-me'>_</span></div>
            </div>
        </div>
    );
};

export default EduRangeHome;