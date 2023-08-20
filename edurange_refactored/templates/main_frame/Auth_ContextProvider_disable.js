// import React from 'react';
// import { useContext } from 'react';
// import { MainFrameContext } from './MainFrame';
// import Login from './components/login/Login';

// export const Auth_ContextProvider = ({ children }) => {

//     const { login_state } = useContext(MainFrameContext);

//     if ( login_state === true) { return children }
//     else { return <Login />; }
// };

    // This is a component that will only Only render its child components if login_state is true.
    // it can be imported into any component and wrapped around routes that should be restricted.
    // users who are not authenticated will be shown the Login.js component.
    //
    // this is only a superficial security measure, however, and data should only be loaded into
    // the browser if the user is expected to see it.  
    // anything that reaches the React environment should be considered as good as exposed (to the user).

    // this boolean is set true by Login.js upon succesful login but will reset to false on refresh at this point
    // roles are not yet well parsed.
