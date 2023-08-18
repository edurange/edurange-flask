"use strict";
import React, { useContext } from 'react';
import { MainFrameContext } from '../../MainFrame';
import { useNavigate } from 'react-router-dom';
import { buildInstructorData } from '../../../../modules/instructor/buildInstructorData';

function Login(props) {
  
  
//HOOKS//////////////////////////////////////

  // hook declarations:
  // imported props:
  const {
    connectIP, connectPort, loginRoute,
    session_csrfToken_state,
    set_session_userData_state,
    set_session_instructorData_state,
    jwt_authenticated_state,
    set_jwt_authenticated_state
    
  } = useContext(MainFrameContext);

  const navigate = useNavigate();

  if (jwt_authenticated_state === true) {navigate('/home_sister/dashboard/');}
  
  async function sendLoginRequest(username_input, password_input) {

    try {
      const response = await fetch(`http://${connectIP}:${connectPort}${loginRoute}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': session_csrfToken_state,

        },
        body: JSON.stringify({
          username: username_input,
          password: password_input,
        }),
      });

      if (!response.ok) { throw new Error('Login failure.'); }

      const responseData = await response.json();
      if (responseData.user) {
        console.log("Login success!");
        console.log("Login responseData: ",responseData);
        const tempInstructorData = buildInstructorData(responseData);
        set_session_instructorData_state(tempInstructorData);
        set_session_userData_state(responseData.user);
        set_jwt_authenticated_state(true);
        navigate('/home_sister/dashboard/');
      }
      else { console.log('Login failure.'); };

    } catch (error) {console.error('Error:', error);}
  }

  const handleSubmit = event => {
    event.preventDefault();
    const usernameInput = event.target.elements.username.value;
    const passwordInput = event.target.elements.password.value;
    sendLoginRequest(usernameInput, passwordInput);
  };  

  return (

    <div className='universal-page-parent'>
      <div className='universal-page-child'>


        <div className='pucs-login-container'>

          <div className='pucs-login-text-frame'>

            <h2 className='pucs-login-text'>Enter your credentials</h2>
          </div>
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

export default Login;
