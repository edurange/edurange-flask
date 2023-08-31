import React from 'react';
import { useContext } from 'react';

import { HomeRouterContext } from '../../pages/home/src/Home_router';
import Login from '../../pages/home/src/components/login/Login';

export const LoggedIn_context = ({ children }) => {

    const login_session = JSON.parse(sessionStorage.getItem('login'));
    const { login_state } = useContext(HomeRouterContext);
    
    const shouldShow = ((login_session === true) || (login_state === true) )
    
    if ( shouldShow === true ) { return children }
    else { return <Login  />; }
};
