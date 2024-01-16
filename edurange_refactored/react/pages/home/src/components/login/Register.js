import React, { useContext } from 'react';

import { HomeRouterContext } from '../../Home_router';
import axios from 'axios';
import './Login.css'
import edurange_icons from '../../../../../modules/ui/edurangeIcons';
// import Login from './Login';
// import { sendLoginRequest } from './Login';

function Register() {

    const {
        set_userData_state, set_login_state,
        updateNav, loginExpiry
    } = useContext(HomeRouterContext);

    async function sendRegistrationRequest(username_input, email_input, password_input, confirm_password_input, code_input) {

        console.log('invoke sendRegistrationRequest()');

        try {
            const response = await axios.post('/register',
                {
                    username: username_input,
                    email: email_input,
                    password: password_input,
                    confirm_password: confirm_password_input,
                    code: code_input // required; generated reference to user groupCode
                }
            );
            const reg_response = response.data;
            const userData = response.data;

            if (reg_response) {
                console.log("Registration Success!");
                console.log("reg_response: ", reg_response);

                // set_userData_state(userData);
                // set_login_state(true);
                // const newExpiry = Date.now() + loginExpiry;
                // sessionStorage.setItem('userData', JSON.stringify(userData));
                // sessionStorage.setItem('navName', `dash`);
                // sessionStorage.setItem('login', true);
                // sessionStorage.setItem('loginExpiry', newExpiry);
                updateNav('/edurange3/login/', 'home');


            } else {
                const errData = response.data.error;
                console.log(errData);
                console.log('Registration failure.');
                
            };
        } catch (error) {
            console.error('Error:', error);
        };
    };

    const handleSubmit = event => {
        event.preventDefault();
        const username_input = event.target.elements.username.value;
        const password_input = event.target.elements.password.value;
        const confirm_password_input = event.target.elements.confirm_password.value;
        const code_input = event.target.elements.code.value;
        const email_input = event.target.elements.email.value;
        sendRegistrationRequest(username_input, email_input, password_input, confirm_password_input, code_input);
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
                    <div className='edu3-login-submit-row-left'>
                        <div className='edu3-login-submit-item'>
                            <label className='edu3-login-prompt-text' htmlFor='confirm_password'>Confirm Password:</label>
                            <input className='edu3-login-input-text' type='password' id='confirm_password' name='confirm_password' />
                        </div>

                        <div className='edu3-login-submit-item'>
                            <label className='edu3-login-prompt-text' htmlFor='email'>Email:</label>
                            <input className='edu3-login-input-text' type='text' id='email' name='email' />
                        </div>
                        <div className='edu3-login-submit-item'>
                            <label className='edu3-login-prompt-text' htmlFor='code'>Code:</label>
                            <input className='edu3-login-input-text' type='text' id='code' name='code' />
                        </div>
                    </div>

                    <div className='edu3-login-submit-row-right'>
                        <button className='edu3-login-button' type='submit'>
                            {edurange_icons.user_check}
                        </button>
                    </div>

                </div>
            </form>
        </div>
    );
};

export default Register;
