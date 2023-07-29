// import React, { useState, useEffect } from 'react';

// async function LoginFromNav() {

//   // useEffect(() => {
//   const csrfTokenInput = document.querySelector('#csrf_token');
//     // if (csrfTokenInput) {
//   const csrfToken = csrfTokenInput.value;
//       console.log('CSRF Token:', csrfToken);
//   // }
//   // }, []);

//   async function sendPostRequest(username, password) {
//     try {
//       const response = await fetch('http://127.0.0.1:8008/home_sister', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//           'X-CSRFToken': csrfToken,
//         },
//         body: JSON.stringify({
//           csrf_token: csrfToken,
//           username: username,
//           password: password,
//         }),
//       });

//       if (!response.ok) {
//         throw new Error('Network response was not ok.');
//       }

//       const data = await response.json();
//       console.log(data);
//     } catch (error) {
//       console.error('Error:', error);
//     }
//   }
  

  // function sendPostRequest(username, password) {
  //   fetch('http://127.0.0.1:8008/home_sister', {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //       'X-CSRFToken': csrfToken,
  //     },
  //     body: JSON.stringify({
  //       csrf_token: csrfToken,
  //       username: username,
  //       password: password,
  //     }),
  //   })
  //     .then(response => console.log(response))
  //     // .then(data => console.log(data))
  //     .catch(error => console.error('Error:', error));
  // }

  // const handleSubmit = event => {
  //   event.preventDefault();
  //   const usernameInput = event.target.elements.username.value;
  //   const passwordInput = event.target.elements.password.value;
  //   sendPostRequest(usernameInput, passwordInput);
  // };

  import React, { useState, useEffect } from 'react';

  async function sendPostRequest(username, password, csrfToken) {
    try {
      const response = await fetch('http://127.0.0.1:8008/home_sister', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });
      console.log(response)
      if (!response.ok) {
        throw new Error('Network response was not ok.');
      }

      const data = response;
      console.log(data);
    } catch (error) {
      console.error('Error:', error);
    }
  }

function LoginFromNav() {
  const [csrfToken, setCsrfToken] = useState(null);

  useEffect(() => {
    const fetchCsrfToken = async () => {
      try {
        const csrfTokenInput = document.querySelector('#csrf_token');
        if (csrfTokenInput) {
          const token = csrfTokenInput.value;
          console.log('CSRF Token:', token);
          setCsrfToken(token);
        }
      } catch (error) {
        console.error('Error fetching CSRF token:', error);
      }
    };

    fetchCsrfToken();
  }, []);

  const handleSubmit = event => {
    event.preventDefault();
    const usernameInput = event.target.elements.username.value;
    const passwordInput = event.target.elements.password.value;
    sendPostRequest(usernameInput, passwordInput, csrfToken);
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
