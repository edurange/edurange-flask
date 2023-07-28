import React, { useState } from 'react';

function LoginFromNav() {
  const [isOpen, setIsOpen] = useState(true);

  function sendPostRequest(username, password) {
    fetch('http://127.0.0.1:8008', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        csrf_token: 'value',
        username: username,
        password: password,
      }),
    })
      .then(response => console.log(response))
      // .then(data => console.log(data))
      .catch(error => console.error('Error:', error));
  }

  const handleSubmit = event => {
    event.preventDefault();
    const usernameInput = event.target.elements.username.value;
    const passwordInput = event.target.elements.password.value;
    sendPostRequest(usernameInput, passwordInput);
  };

  const closeModal = () => {
    setIsOpen(false);
  };

  return (
    <div className='universal-tab-parent'>
      <div className='universal-tab-container'>
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
