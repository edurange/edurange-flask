
//  we are using axios so this is no longer needed.
//  will keep for reference for the time being.

async function fetchHelper (methodArg, fetchBody, csrf) {

  const fetchURL = "http://127.0.0.1/edurange3/"; // update as needed

  const currentCSRF = await csrf;

  const fetchOptions = {
    method: methodArg,
    credentials: 'include',    // very important!
    headers: {
        'Content-Type': 'application/json',
        'X-XSRF-TOKEN': currentCSRF,
    }
};
if (methodArg !== 'GET' && methodArg !== 'HEAD') {
  fetchOptions.body = JSON.stringify(fetchBody);
}

  try {
    const response = await fetch(`${fetchURL}`,fetchOptions);
    if (!response.ok) { return { "error" : response.status }; };
    const jsonData = await response.json();
    console.log("fetchHelper return: ",jsonData);
    return jsonData;

  } catch (error) { console.error('fetchHelper error:', error); }
};
  export default fetchHelper;