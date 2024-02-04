

export async function sendLoginRequest(username_input, password_input) {
    try {
      const response = await axios.post('/login',
        {
          username: username_input,
          password: password_input
        }
      );
      const userData = response.data;
  
      if (userData) {
        console.log("Login success!");
        console.log("Login userData", userData);
        set_userData_state(userData);
        set_login_state(true);
        const newExpiry = Date.now() + loginExpiry;
        sessionStorage.setItem('userData', JSON.stringify(userData));
        sessionStorage.setItem('navName', `dash`);
        sessionStorage.setItem('login', true);
        sessionStorage.setItem('loginExpiry', newExpiry);
        updateNav('/edurange3/dashboard/', `dash`);
      } else {
        const errData = response.data.error;
        console.log(errData);
        console.log('Login failure.');
      };
    } catch (error) {
      console.error('Error:', error);
    };
  };