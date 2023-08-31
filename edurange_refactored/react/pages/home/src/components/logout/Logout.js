import React, {useEffect, useContext} from 'react';
import axios from 'axios';
import { HomeRouterContext } from '../../Home_router';

function Logout () {

    const { 
        set_userData_state, 
        login_state, 
        set_login_state 
    } = useContext(HomeRouterContext);

    async function sendLogoutRequest() {
        try {
            const response = await axios.post('/api/logout');
            const responseData = response.data;

            if (responseData.message) {
                console.log("Logout success!");
                console.log("Logout message: ", responseData.message);
                set_userData_state({});
                set_login_state(false);
            sessionStorage.setItem('login', false);
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

    if (login_state) {return (<>You have NOT been logged out!.</>)}
    return (<>You have been successfully logged out!</>);
}

export default Logout;
