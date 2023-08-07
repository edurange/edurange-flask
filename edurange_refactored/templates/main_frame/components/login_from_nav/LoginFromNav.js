"use strict";
import React, { useContext } from 'react';
import { MainFrameContext } from '../../MainFrame';
import * as loginHelper from './loginHelper';

import DevTable from '../temp/DevTable';


function LoginFromNav(props) {
  
  
//HOOKS//////////////////////////////////////

  // hook declarations:

  // imported props:
  const {
    activeTab_state,  update_tabChoice_status,
    login_state,      update_login_status,
    csrfToken_state,  update_csrfToken_status,
    connectIP, connectPort, loginRoute,
    session_userInfo_state, set_session_userInfo_state,
    session_instructorData_state, set_session_instructorData_state
  } = useContext(MainFrameContext);

/////////////////////////////////////////////

  if (login_state === 1) {return (
    <DevTable/>
  )};

  
  async function sendLoginRequest(username_input, password_input, csrfToken_state) {

    try {
      const response = await fetch(`http://${connectIP}:${connectPort}${loginRoute}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'csrf_token_sister': csrfToken_state
        },
        body: JSON.stringify({
          username: username_input,
          password: password_input,
        }),
      });

      if (!response.ok) { throw new Error('Login failure.'); }

      const data = await response.json();

      if (data.user) {
        console.log("Login success!");
        const betterData = loginHelper.recombobulate(data);
        console.log("recombobulated data from LoginFromNav",betterData)
        set_session_instructorData_state(betterData)
        update_login_status(1);
      }
      else { console.log('Login failure.'); };

    } catch (error) {console.error('Error:', error);}
  }

  const handleSubmit = event => {
    event.preventDefault();
    const usernameInput = event.target.elements.username.value;
    const passwordInput = event.target.elements.password.value;
    sendLoginRequest(usernameInput, passwordInput, csrfToken_state);
  };
  return (

    <div className='universal-page-parent'>
      <div className='universal-page-child'>


        <div className='login-container'>

          <h2>Enter your credentials</h2>
          <form onSubmit={handleSubmit}>

            <div>
              <label htmlFor='username'>Username:</label>
              <input type='text' id='username' name='username' />
            </div>

            <div>
              <label htmlFor='password'>Password:</label>
              <input type='password' id='password' name='password' />
            </div>

            <button type='submit'>Submit</button>
            
          </form>

        </div>

      </div>
    </div>

  );
}

export default LoginFromNav;
