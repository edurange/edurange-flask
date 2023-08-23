
//  we are using axios so this is no longer needed.
//  will keep for reference for the time being.

async function fetchHelper (methodArg, fetchRoute, fetchBody, csrf) {

  const fetchURL = "https://riparian.dev"; // or whatever your edurange IP/domain is
  const connectPort = "5000"; // or whatever your edurange port is

  const currentCSRF = await csrf;

  const fetchOptions = {
    method: methodArg,
    credentials: 'include',    // very important!
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': currentCSRF,
    }
};
if (methodArg !== 'GET' && methodArg !== 'HEAD') {
  fetchOptions.body = JSON.stringify(fetchBody);
}

  try {

    const response = await fetch(`${fetchURL}${fetchRoute}`, fetchOptions);
    
    if (!response.ok) { return { "error" : response.status }; };

    const jsonData = await response.json();
    console.log("fetchHelper return: ",jsonData);
    return jsonData;

  } catch (error) { console.error('fetchHelper error:', error); }
};
  export default fetchHelper;