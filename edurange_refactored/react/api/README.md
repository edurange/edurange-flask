




let's start adding meta info for these types of notes. 
here's one way we could do it



-README-8.22.23------------------------

The `/edurange_refactored/react/api` folder is for all of 
the React->Flask API specific things that may be accessed by
multiple scripts.

That should include all of the API fetch requests
any of our components need, so we can all have access to them, 
rather than spending time creating functions for API calls that
someone else already wrote.

That being said, if updates to existing routes are needed, it is
a good idea to just make a new route (and/or file) rather than 
changing one that might already be in use, or might be needed later,
unless of course it is determined that the old one is deprecated.

-------------------------------------------



-AXIOS-8.22.23-------------------------------

Subjects: axios, React->Flask API calls
Key Files: AxiosConfig.js, EduRangeEntry.js

axios is now enabled for most API / AJAX calls!

Axios is a library that will allow us to predefine some of the 
more annoying boilerplate things that our setup needs, 
such as including CSRF and JWT tokens in header for validation.

It is non-intrusive and optional, but extremely handy, and usage is 
very similar to standard fetch() API in most ways, except you 
don't need to write 50 lines of boilerplate.

    AxiosConfig.js is a 'wrapper' React component which initializes
    and configures axios for edurange3.  All of the token and header
    settings have already been set up, and automated. Simply use
    the `axios.get` or `axios.post` (etc) methods, and bingo. (example below)

On the backend (flask), the routes are also automatically auth'd
with the use of the @jwt_and_csrf_required decorator function.
    
TLDR: With axios, you no longer have to worry about tokens or special 
headers in order to make protected API call functions in React
or their matching auth protected routes in Flask!

example usage in a React component:
...
import axios from 'axios';
...
...
...
    try {
        const response = await axios.post('login',
            {
            username: username_input,
            password: password_input
            }
        );
        const responseData = response.data;
        if (responseData.user_data) {console.log("Login success!");} 
        else {console.log('Login failure.');
    } 
    catch (error) {console.error('Error:', error);};
    };
...
...
...
note: the use of `await` in React usually involves a `useEffect()` hook.
this is my preferred Promise syntax, but you can probably use `.then` syntax
and avoid using `useEffect()`

note2: this .post axios method is for POST requests. 
But GET (.get), DELETE (.delete), etc methods are avail as well.

-----------------------------------------