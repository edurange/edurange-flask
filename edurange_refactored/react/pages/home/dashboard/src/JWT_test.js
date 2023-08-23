import React, { useEffect, useState } from 'react';
import axios from 'axios';

// Removed the unused HomeRouterContext import
// import { useAxios } from '../../../../api/config/axiosConfig';
function JWT_Test() {
    // const myAx = useAxios;
    // const axi = myAx();

    const [testResponse, set_testResponse] = useState({
        username: "bub",
        user_id: null,
        user_role: "none",
        message: "Go away"
    });

    useEffect(() => {

        async function beginFetch() {
            try {
                const response = await axios.post("api/jwt_test");
                console.log("RESPONSE FROM AFTER JWT_TEST REQ", response);
                
                if (response.data.user_id) {
                    set_testResponse(response.data);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }

        beginFetch();

    }, []); // This ensures that the effect will re-run if axi changes.

    console.log("TRYING TO RUN JWT TEST IN COMPONENT");
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