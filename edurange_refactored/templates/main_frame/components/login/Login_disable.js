// "use strict";
// import React, { useContext, useEffect } from 'react';
// import { MainFrameContext } from '../../MainFrame';
// import { useNavigate } from 'react-router-dom';
// import { buildInstructorData } from '../../../../react/modules/utils/buildInstructorData';

// function Login() {

//   const {
//     connectIP, connectPort, loginRoute,
//     session_csrfToken_state,
//     set_session_userData_state,
//     set_session_instructorData_state,
//     set_login_state

//   } = useContext(MainFrameContext);

//   const navigate = useNavigate();

//   async function sendLoginRequest(username_input, password_input) {

//     try {
//       const response = await fetch(`http://${connectIP}:${connectPort}${loginRoute}`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//           'X-CSRFToken': session_csrfToken_state,

//         },
//         body: JSON.stringify({
//           username: username_input,
//           password: password_input,
//         }),
//       });

//       if (!response.ok) { throw new Error('Login failure.'); }

//       const responseData = await response.json();
//       if (responseData.user) {
//         console.log("Login success!");
//         console.log("Login responseData: ", responseData);
//         const tempInstructorData = buildInstructorData(responseData);
//         set_session_instructorData_state(tempInstructorData);
//         set_session_userData_state(responseData.user);
//         set_login_state(true);
//         const currentTime = new Date();
//         const userSession = {
//           isLoggedIn: true,
//           expiry: Date.now() + 36000000 // expires in 10 hrs
//       };
//       sessionStorage.setItem('edurange3_session', JSON.stringify(userSession));
      
//         navigate('/edurange3/dashboard/');
//       }
//       else { console.log('Login failure.'); };

//     } catch (error) { console.error('Error:', error); }
//   }

//   const handleSubmit = event => {
//     event.preventDefault();
//     const usernameInput = event.target.elements.username.value;
//     const passwordInput = event.target.elements.password.value;
//     sendLoginRequest(usernameInput, passwordInput);
//   };

//   return (

//     <div className='universal-page-parent'>
//       <div className='universal-page-child'>
//         <div className='pucs-login-container'>
//           <div className='pucs-login-text-frame'>
//             <h2 className='pucs-login-text'>Enter your credentials</h2>
//           </div>
//           <form onSubmit={handleSubmit}>

//             <div>
//               <label htmlFor='username'>Username:</label>
//               <input type='text' id='username' name='username' />
//             </div>

//             <div>
//               <label htmlFor='password'>Password:</label>
//               <input type='password' id='password' name='password' />
//             </div>

//             <button type='submit'>Submit</button>
//           </form>
//         </div>
//       </div>
//     </div>

//   );
// }

// export default Login;
