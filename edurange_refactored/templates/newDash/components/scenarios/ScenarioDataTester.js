
import React, { useState } from 'react';

function ScenarioDataTester() {
  const [data, setData] = useState(null);

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8008/home_sister/api/get_scenario', {
        method: 'POST',
        headers: {
          // 'Accept': 'application/json',          // Expecting JSON response
          'Content-Type': 'application/json',   // Sending JSON data
          // 'Custom-Header': 'custom-value'
        },
        body: JSON.stringify({ userID: 2 }) // Replace with your actual data if needed
      });
      
      console.log(response);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const jsonData = await response.json();
      setData(jsonData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div>
      <button onClick={fetchData}>Fetch Data</button>
      
      {data && (
        <div>
          <h3>User Info</h3>
          <p>ID: {data.userInfo?.id}</p>
          <p>Username: {data.userInfo?.username}</p>
          <p>Email: {data.userInfo?.email}</p>

          <h3>Groups</h3>
          {data.groups?.map(group => (
            <div key={group.id}>
              <p>ID: {group.id}</p>
              <p>Name: {group.name}</p>
            </div>
          ))}

          <h3>Scenario Table</h3>
          {data.scenarioTable?.map(scenario => (
            <div key={scenario.id}>
              <p>ID: {scenario.id}</p>
              <p>Name: {scenario.sname}</p>
              <p>Type: {scenario.type}</p>
              <p>Group Name: {scenario.gname}</p>
              <p>Owner Username: {scenario.iname}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ScenarioDataTester;