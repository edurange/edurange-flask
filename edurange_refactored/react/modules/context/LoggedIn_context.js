// IS IN USE

import React from 'react';
import { useContext } from 'react';

import { HomeRouterContext } from '../../pages/home/src/Home_router';
import Login from '../../pages/home/src/components/login/Login';

export const LoggedIn_context = ({ children }) => {

    const { login_state } = useContext(HomeRouterContext);

    if ( login_state === true) { return children }
    else { return <Login  />; }
};
