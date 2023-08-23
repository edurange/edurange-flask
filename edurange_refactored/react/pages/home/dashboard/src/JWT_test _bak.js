import React, { useContext, useEffect, useState } from 'react';
import { HomeRouterContext } from '../../src/Home_router';
import fetchHelper from '../../../../api/common/fetchHelper';

function JWT_Test() {

    const { csrfToken_state } = useContext(HomeRouterContext);
    const [testResponse, set_testResponse] = useState({
        username: "bub",
        user_id: null,
        user_role: "none",
        message: "Go away"
    });
    
    useEffect(() => {
        if (!csrfToken_state) return;  // abort if no csrf
        async function beginFetch() {
            try {
                const response = await fetchHelper(
                    "POST",
                    "/edurange3/api/jwt_test",
                    {},
                    csrfToken_state
                );
                if (response.user_id) {
                    console.log( response )
                    set_testResponse(response) };
                // return response;

            } catch (error) { console.error('Error fetching data:', error); }

        };
        beginFetch();
    }, [csrfToken_state]);
    console.log("TRYING TO RUN JWT TEST IN COMPONENT")
    return (
        <>THIS IS THE JWT_Test!
            <br></br>
            <br></br>
            <h1>{testResponse.message}, {testResponse.username}!</h1>
            <br></br>
            <br></br>
            <h1>Your ID is {testResponse.user_id}</h1>
            <br></br>
            <br></br>
            <h1>Your role is {testResponse.user_role}</h1>
        </>
    );
};
export default JWT_Test;