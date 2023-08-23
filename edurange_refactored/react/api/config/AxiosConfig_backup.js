import { useEffect, useState } from 'react';
import axios from 'axios';

const baseURL = 'https://riparian.dev/edurange3/';

// w/ this config, all requests include CSRF token in header by default.
// getCSRF() is needed bc of timing issues when the document is queried.

export async function getCSRF() {
  try {
      const embeddedCSRF = document.querySelector('meta[name="EMBEDDED_CSRF"]');
      if (embeddedCSRF) {
          console.log(`getCSRF has found the token value: ${embeddedCSRF.content}`)
          return embeddedCSRF.content;
      } else {
          throw new Error("CSRF token not found");
      }
  } catch (error) {
      console.log(error);
      return null;
  };
};

const AxiosConfig = ({ children }) => {
  const [csrfToken_state, set_csrfToken_state] = useState(null);
  const [mounted_state, set_mounted_state] = useState(false);

  useEffect(() => {
    async function getToken() {
      try {
        
        const returned_csrf = await getCSRF();
        set_csrfToken_state( returned_csrf);
        set_mounted_state(true);

      } catch (error) {
        console.log(error);
      }
    };
    getToken();
    
  }, []);

//  caveat dev: 
//  X-XSRF-TOKEN seems to be an axios keyword of sorts; woe to renamers.
  useEffect(() => {
    axios.defaults.baseURL = baseURL;
    axios.defaults.headers.common['X-XSRF-TOKEN'] = csrfToken_state;
    axios.defaults.withCredentials = true;
  }, [mounted_state]);

  return children;
};
export default AxiosConfig;
