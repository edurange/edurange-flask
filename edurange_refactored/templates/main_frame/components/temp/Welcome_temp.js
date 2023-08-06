"use strict";
import React, { useContext } from 'react';
import ConnectionInfo from '../connection_info/ConnectionInfo';
import { MainFrameContext } from '../../MainFrame';
import { recombobulate, convertToDivs } from '../login_from_nav/loginHelper';
function Welcome_temp() {
   

//HOOKS//////////////////////////////////////

  // hook declarations:

  // imported props:
  const { session_userInfo_state, session_instructorData_state } = useContext(MainFrameContext);

/////////////////////////////////////////////

    // const neatoDisplay = JSON.stringify (session_instructorData_state);
    // const neato2Display = JSON.stringify (recombobulate(session_instructorData_state));
    // const neato2 = convertToDivs(neatoDisplay);

    return (
        <div className='universal-page-parent'>
            <div className='universal-page-child'>
                <h1>WELCOME TO EDURANGE!!!!</h1>
                <h1>User:               {session_userInfo_state.username || "none"}</h1>
                <h1>Creation Time:      {session_userInfo_state.created_at || "none"}</h1>
                <h1>email:              {session_userInfo_state.email || "none"}</h1>
                <h1>role:               {session_userInfo_state.role || "none"}</h1>
                <h1>Instructor?:        {(session_userInfo_state.role === "Instructor" || session_userInfo_state.role === "Administrator") ? "Hello professor" : "Nope."}</h1>
                <h1>Admin?              {session_userInfo_state.role === "Administrator" ? "Hello admin" : "Nope."}</h1>
                {/* <h1>String Time!        { neato2 }</h1> */}
                <ConnectionInfo/>
            </div>
        </div>
    );
};

export default Welcome_temp;