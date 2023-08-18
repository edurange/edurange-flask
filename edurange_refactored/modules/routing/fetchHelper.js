import React, {useState, useContext} from 'react';

export async function fetchData (method, fetchRoute, fetchBody, edurange_csrf, edurange_jwt) {

    // console.log(session_jwt_token_state)

    try {
      const response = await fetch(`http://127.0.0.1:8008/${fetchRoute}`, {
        method: method,
        headers: {
          'Content-Type': 'application/json',   // designate req as JSON data
          'Authorization': `${jwt}`,   // add JWT to header ('Authorization' key is important to Flask_JWT_simple, so don't change!)
          'csrf_token_sister': `${csrf}`   // Sending CSRFT
        },
        body: JSON.stringify(fetchBody)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const jsonData = await response.json();
      console.log(jsonData);
      return jsonData;
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  