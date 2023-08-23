import axios from 'axios';
import React, { useEffect, useState } from 'react';

function JWT_Test() {

    const [testResponse, set_testResponse] = useState({
        username: "bub",
        user_id: null,
        user_role: "none",
        message: "Go away"
    });

    useEffect(() => {
        async function beginFetch() {
            try {
                const response = await axios.post("/api/jwt_test");
                if (response.data.user_id) {
                    set_testResponse(response.data);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
        beginFetch();
    }, []);

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