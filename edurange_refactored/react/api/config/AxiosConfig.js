import axios from 'axios';
import { useEffect } from 'react';

const baseURL = 'http://10.0.0.55:5000/edurange3/';

function getCSRFTokenFromCookie() {
    const name = 'X-XSRF-TOKEN';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        const cookieReturn = parts.pop().split(';').shift();
        console.log (cookieReturn)
        return cookieReturn }
    return null;
}
const csrfToken = getCSRFTokenFromCookie();

if (!csrfToken) {console.log('CSRF token not found in cookie');} // DEV_ONLY
else {
    axios.defaults.baseURL = baseURL;
    axios.defaults.headers.common['X-XSRF-TOKEN'] = csrfToken;
    axios.defaults.withCredentials = true;
}
const AxiosConfig = ({ children }) => {
    return children;
};

export default AxiosConfig;