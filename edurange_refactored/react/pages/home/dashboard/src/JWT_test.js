import React, {useContext, useEffect, useState} from 'react';
import { HomeRouterContext } from '../../src/Home_router';

// this is only a testing component, the real auth provider component is Auth_ContextProvider.js

function JWT_Test ( ) {

    const { session_csrfToken_state } = useContext(HomeRouterContext);

    const [demo_user, set_demo_user] = useState("No one");

    useEffect(() => {

        async function fetchDataFromApi() {
            try {
                const response = await fetch (`http://127.0.0.1:8008/edurange3/dashboard/jwt_auth`,
                
                {    
                    method: 'POST',
                    credentials: 'include',    // very important! 
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': session_csrfToken_state,
                        // any additional 'headers' properties
                    },                              
                    body: JSON.stringify({
                        "message": 'anything else',
                        "test2": "value2"
                        
                        // any additional 'body' properties
                    })                  
                }
                )

            if (!response.ok) { throw new Error(`HTTP error! Status: ${response.status}`); }
        
            const jsonData = await response.json();
            console.log("JWT_Test REPORTING RETURN: ",jsonData);
            set_demo_user(jsonData.message)
            return jsonData;

            } catch (error) { console.error('Error fetching data:', error); }
            
        }; 
        fetchDataFromApi();
    }, []);
    return (
        <>THIS IS THE JWT_Test! 
        <br></br>
        <h1>hello, {demo_user}</h1>
        </>
    );
};  
export default JWT_Test;