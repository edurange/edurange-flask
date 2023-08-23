import React, { useContext, useEffect } from 'react';

import { useNavigate } from 'react-router-dom';
import { HomeRouterContext } from '../../Home_router';
import { buildInstructorData } from '../../../../../modules/scenarios/buildInstructorData'
import axios from 'axios';

const loginExpiry = (1000 * 60 * 60 * 1); // 1 hr in miliseconds

function Login() {

  const {
    set_userData_state,
    set_instructorData_state,
    set_login_state

  } = useContext(HomeRouterContext);

  const navigate = useNavigate();

  async function sendLoginRequest(username_input, password_input) {
    try {
      const response = await axios.post('login',
        {
          username: username_input,
          password: password_input
        }
      );
  
      const responseData = response.data;
  
      if (responseData.user_data) {
        console.log("Login success!");
        console.log("Login responseData: ", responseData);
        const tempInstructorData = buildInstructorData(responseData);
        set_instructorData_state(tempInstructorData);
        set_userData_state(responseData.user_data);
        set_login_state(true);
        const userSession = {
          isLoggedIn: true,
          expiry: Date.now() + loginExpiry
        };
        sessionStorage.setItem('edurange3_session', JSON.stringify(userSession));
        navigate('/edurange3/dashboard/');
      } else {
        const errData = responseData.error;
        console.log(errData);
        console.log('Login failure.');
      };
    } catch (error) {
      console.error('Error:', error);
    };
  };

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
};

export default Login;
