




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
Key Files: axiosConfig.js

Axios is a library that will allow us to predefine some of the 
more annoying boilerplate things that our setup is using, 
including CSRF token validation

It is non-intrusive and optional, but extremely handy, and usage is 
very similar to standard fetch() API in most ways.

An instance (returned from `useAxios()`) that has been 
initialized to eduRange values (including CSRF and error handling. 
etc).  To use it, import `useAxios` from axiosConfig.js

example usage in a React component:

import { useAxios } from '/path/to/edurange_refactored/react/api/config/axiosConfig'

MyComponent () {

    myAxios = useAxios();

    myReturn = myAxios.get( ...etc... )  

    return (<>{myReturn.message}</>)
}

as you probably guessed, this axios method is for GET requests. 
But POST (.post), DELETE (.delete), etc methods are avail as well.

-----------------------------------------