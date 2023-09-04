import React, {useEffect, useContext} from 'react';
import axios from 'axios';
import { HomeRouterContext } from '../../Home_router';

function Logout () {

    const { 
        set_userData_state, 
        login_state, 
        set_login_state ,
        set_navName_state,

    } = useContext(HomeRouterContext);

    async function sendLogoutRequest() {
        try {
            const response = await axios.post('/api/logout');
            const responseData = response.data;

            if (responseData.message) {
                console.log("Logout success!");
                console.log("Server Response: ", responseData.message);
                set_userData_state({});
                set_login_state(false);
                set_navName_state('logout')
            sessionStorage.setItem('login', false);
            sessionStorage.setItem('loginExpiry', 0);
            sessionStorage.setItem('userData', '{}');
            sessionStorage.setItem('navName','logout')
            }
            else {
                const errData = responseData.error;
                console.log(errData);
                console.log('Logout failure.');
            };
        }
        catch (error) {
            console.error('Error logging out:', error);
        };
    };

    useEffect(() => {sendLogoutRequest();}, []);

    if (login_state) {return (<h1>You are NOT logged out!</h1>)}
    return (<h1>You are currently logged out.</h1>);
}

export default Logout;
