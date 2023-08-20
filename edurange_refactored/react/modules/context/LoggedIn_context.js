import React from 'react';
import { useContext } from 'react';

import { HomeRouterContext } from '../../pages/home/src/Home_router';
import Login3 from '../../pages/home/src/components/login/Login3';

export const LoggedIn_context = ({ children }) => {

    const { login_state } = useContext(HomeRouterContext);

    if ( login_state === true) { return children }
    else { return <Login3  />; }
};
