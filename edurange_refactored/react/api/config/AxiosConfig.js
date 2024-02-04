
// SECURITY WARNING
// It is very important that the CSRF token value is NOT submitted
// as a cookie, but rather in a request header, body, or footer.
// 
// The reason: Cookies can be submitted automatically on behalf of
// a victim's browser in the case of CSRF attacks. To prevent this,
// edurange3 is set up so that CSRF token value is read from the
// header, and not the cookie (unlike our auth JWT).
//
// If edurange3 were set up to accept the cookie value as the CSRF
// being submitted, a CSRF check would be mostly self-defeating.
//
// TLDR: If you change how the CSRF token is submitted/accepted, 
//       do NOT make it by way of cookie.

import axios from 'axios';

function getCSRFfromCookie() {
    const name = 'X-XSRF-TOKEN';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        const cookieReturn = parts.pop().split(';').shift();
        return cookieReturn; 
    };
    return null;
};
const csrfToken = getCSRFfromCookie();

// By the time you see this, the baseURL should be your own.
// if it is incorrect (or says URL_TO_BE_REPLACED), you must
// update that portion to your actual edurange instance IP.
// example:
const baseURL = 'http://URL_TO_BE_REPLACED:5000/edurange3/'; 

if (!csrfToken) { 
    console.log('Axios: CSRF cookie not found'); } // DEV_ONLY

axios.defaults.baseURL = baseURL;
axios.defaults.headers.common['X-XSRF-TOKEN'] = csrfToken || ""; // provide empty for login
axios.defaults.withCredentials = true; // very important

const AxiosConfig = ({ children }) => {

    return children;
};

export default AxiosConfig; 
