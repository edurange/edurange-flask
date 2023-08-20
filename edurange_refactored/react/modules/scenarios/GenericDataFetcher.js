
import React, { useState } from 'react';

function GenericDataFetcher() {
  const [data, setData] = useState(null);

  const fetchData = async (fetchRoute, fetchBody) => {
    try {
      const response = await fetch(`http://127.0.0.1:8008/edurange3/api/${fetchRoute}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',   // Sending JSON data
        },
        body: JSON.stringify(fetchBody)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const jsonData = await response.json();
      setData(jsonData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const renderData = (key, value) => {
    // Base case: if the value is a simple type, just render it
    if (typeof value !== 'object' || value === null) {
      return <p key={key}>{key}: {value}</p>;
    }
    
    // If value is an array, we'll map over its items and render them recursively
    if (Array.isArray(value)) {
      return (
        <div key={key}>
          <h3>{key}</h3>
          {value.map((item, index) => (
            <div key={index}>
              {Object.entries(item).map(([subKey, subValue]) => renderData(subKey, subValue))}
            </div>
          ))}
        </div>
      );
    }

    // If the value is an object, we'll render its properties recursively
    return (
      <div key={key}>
        <h3>{key}</h3>
        {Object.entries(value).map(([subKey, subValue]) => renderData(subKey, subValue))}
      </div>
    );
  };

  // The following button click won't work as-is because fetchData needs arguments. 
  // This is just a placeholder and should be adjusted according to your use-case
  return (
    <div>
      <button onClick={() => fetchData('someRoute', { someKey: 'someValue' })}>Fetch Data</button>
      
      {data && (
        <div>
          {Object.entries(data).map(([key, value]) => renderData(key, value))}
        </div>
      )}
    </div>
  );
}

export default GenericDataFetcher;


// import React, { useState } from 'react';

// function GenericDataFetcher () {
//   const [data, setData] = useState(null);

//   async function fetchData (fetchRoute, fetchBody) {
//     try {
//       const response = await fetch(`http://127.0.0.1:8008/edurange3/api/${fetchRoute}`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',   // Sending JSON data
//         },
//         body: JSON.stringify(fetchBody) 
//       });
      
//       if (!response.ok) {
//         throw new Error(`HTTP error! Status: ${response.status}`);
//       }

//       const jsonData = await response.json();
//       setData(jsonData);
//     } catch (error) {
//       console.error('Error fetching data:', error);
//     }
//   };

//   const renderData = (key, value) => {
//     if (Array.isArray(value)) {
//       return (
//         <div key={key}>
//           <h3>{key}</h3>
//           {value.map((item, index) => (
//             <div key={index}>
//               {Object.entries(item).map(([subKey, subValue]) => (
//                 <p key={subKey}>{subKey}: {subValue}</p>
//               ))}
//             </div>
//           ))}
//         </div>
//       );
//     } else if (typeof value === 'object') {
//       return (
//         <div key={key}>
//           <h3>{key}</h3>
//           {Object.entries(value).map(([subKey, subValue]) => (
//             <p key={subKey}>{subKey}: {subValue}</p>
//           ))}
//         </div>
//       );
//     }
//     return <p key={key}>{key}: {value}</p>;
//   };

//   return (
//     <div>
//       <button onClick={fetchData}>Fetch Data</button>
      
//       {data && (
//         <div>
//           {Object.entries(data).map(([key, value]) => renderData(key, value))}
//         </div>
//       )}
//     </div>
//   );
// }

// export default GenericDataFetcher
// ;