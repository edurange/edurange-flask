"use strict";
import React, { useState, useEffect, useContext } from 'react';
import { MainFrameContext } from '../../MainFrame';



function LoginFromNav(props) {

  const {
    activeTab_state,update_chosenTab_status,
    login_state, update_login_status,
    update_csrfToken_status,csrfToken_state
  } = useContext(MainFrameContext);

  async function sendPostRequest(username, password, csrfToken_state) {

    try {
      const response = await fetch('http://127.0.0.1:8008/home_sister', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken_state,
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      if (!response.ok) { throw new Error('Login failure.'); }

      const data = await response.json();

      if (data.login_success === "true") {
        console.log("Login success!");
        update_login_status(1);
        update_chosenTab_status(2);
      }
      else { console.log('Login failure.'); };

    } catch (error) {
      console.error('Error:', error);
    }
  }

  useEffect(() => {
    const fetch_csrfToken = async () => {
      try {
        const csrfTokenInput = document.querySelector('#csrf_token');
        if (csrfTokenInput) {
          const token = csrfTokenInput.value;
          update_csrfToken_status(token);
        }
      } catch (error) {
        console.error('Error fetching CSRF token:', error);
      }
    };

    fetch_csrfToken();
  }, []);

  const handleSubmit = event => {
    event.preventDefault();
    const usernameInput = event.target.elements.username.value;
    const passwordInput = event.target.elements.password.value;
    sendPostRequest(usernameInput, passwordInput, csrfToken_state);
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
