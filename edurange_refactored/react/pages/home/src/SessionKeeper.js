
import React, {useContext, useEffect} from 'react';

import { HomeRouterContext } from "./Home_router";
import Login from './components/login/Login';
export const SessionContext = React.createContext();

function SessionKeeper () {

    const { 
        login_state,    set_login_state,
        navName_state,  set_navName_state,
        userData_state, set_userData_state
      } = useContext(HomeRouterContext);
    
    function restoreSession () {
        console.log('Restoring session...');
        
        const loginBoolString = sessionStorage.getItem('login');
        const expiryString = sessionStorage.getItem('loginExpiry');
        
        if (!loginBoolString || !expiryString)  { return <Login/>; };
    
        const expiry = JSON.parse(expiryString);
        const loginBool = JSON.parse(loginBoolString);
        
        if ((!loginBool) || (expiry < Date.now())) { return <Login/>; };
        
        const userDataString = sessionStorage.getItem('userData');
        const navNameString = sessionStorage.getItem('navName');
        
        if ( !userDataString || !navNameString ) { return <Login/>; };
        
        const userData = JSON.parse(userDataString);
        const navName = JSON.parse(navNameString);
        
        set_userData_state(userData);
        set_login_state(true);
        set_navName_state(navName);
      };
      useEffect(() => {restoreSession();}, []);
  };
  export default SessionKeeper;

 