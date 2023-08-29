import React, { useContext } from 'react';

import { useNavigate } from 'react-router-dom';
import { HomeRouterContext } from '../../Home_router';
import axios from 'axios';
import './Login.css'
import { FaUserCheck } from 'react-icons/fa6';

const loginExpiry = (1000 * 60 * 60 * 1); // 1 hr in miliseconds

function Login() {

  const { set_userData_state, set_login_state } = useContext(HomeRouterContext);

  const navigate = useNavigate();

  async function sendLoginRequest(username_input, password_input) {
    try {
      const response = await axios.post('/login',
        {
          username: username_input,
          password: password_input
        }
      );
  
      const responseData = response.data;
  
      if (responseData.user_data) {
        console.log("Login success!");
        console.log("Login responseData: ", responseData);
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
        <div className='edu3-login-container'>
          
            <h2 className='edu3-login-placard'>
              <div className='edu3-login-placard-text'>
                Enter your credentials
              </div>
            </h2>
          
          <form className='edu3-login-submit-frame' onSubmit={handleSubmit}>
          <div className='edu3-login-submit-row'>
              
              <div className='edu3-login-submit-row-left'>
                <div className='edu3-login-submit-item'>
                  <label className='edu3-login-prompt-text' htmlFor='username'>Username:</label>
                  <input className='edu3-login-input-text' type='text' id='username' name='username' />
                </div>

                <div className='edu3-login-submit-item'>
                  <label className='edu3-login-prompt-text' htmlFor='password'>Password:</label>
                  <input className='edu3-login-input-text' type='password' id='password' name='password' />
                </div>
              </div>

              <div className='edu3-login-submit-row-right'>
                <button className='edu3-login-button' type='submit'>
                  <FaUserCheck/>
                </button>
              </div>

          </div>
          </form>
        </div>
  );
};

export default Login;
