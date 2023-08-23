import { useEffect } from 'react';
import axios from 'axios';

const baseURL = 'https://riparian.dev/edurange3/';

// Get the CSRF token from the cookie
function getCSRFTokenFromCookie() {
    const name = 'edurange_csrf';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

const AxiosConfig = ({ children }) => {
    useEffect(() => {
        const csrfToken = getCSRFTokenFromCookie();

        if (!csrfToken) {
            console.error('CSRF token not found in cookie');
            return;
        }

        // Set Axios defaults
        axios.defaults.baseURL = baseURL;
        axios.defaults.headers.common['edurange_x_csrf'] = csrfToken;
        axios.defaults.withCredentials = true;

    }, []); 

    return children;
};

export default AxiosConfig;
