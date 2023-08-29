
// import React, {useState, useContext} from 'react';
// import axios from 'axios';

// const baseURL = 'https://riparian.dev/edurange3/api/'

// function AxiosTestChild1() {

//     const [childContent, set_childContent] = useState( <>Nothing in AxiosTestChild1</> );
//     const { csrfToken_state } = useContext(HomeRouterContext);


//     const axiosInstance =  axios.create({
//         baseURL: baseURL,
//         withCredentials: true,
//         timeout: 700,
//         headers: {'edurange3_csrf': csrfToken_state}
//       });
    
//     return (
//         <>
//             {childContent}
//         </>
//     );
// };

// export default AxiosTestChild1;