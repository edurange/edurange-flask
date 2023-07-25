import React, { useState } from 'react';
import Modal from 'react-modal';

Modal.setAppElement('#root');

function LoginFromWelcome() {
  const [isOpen, setIsOpen] = useState(true);

  const closeModal = () => {
    setIsOpen(false);
  };

  return (
    <div className='universal-tab-container'>
      <div className='centerized-container'>
        <div className='login-container'>

        <h2>Enter your credentials</h2>
          <form>
            <div>
              <label htmlFor="username">Username:</label>
              <input type="text" id="username" name="username" />
            </div>
            <div>
              <label htmlFor="password">Password:</label>
              <input type="password" id="password" name="password" />
            </div>
            <button type="submit">Submit</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default LoginFromWelcome;
