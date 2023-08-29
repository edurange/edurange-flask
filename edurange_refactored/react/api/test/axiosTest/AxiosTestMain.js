

// import React, {useState, useContext} from 'react';
// import AxiosTestChild1 from './AxiosTestChild1';
// import AxiosTestChild2 from './AxiosTestChild2';
// import { useAxios } from '../../config/axiosConfig'; 
// // import axios instance initialized with edurange3 values

// function AxiosTestMain() {

//     const axi = useAxios(); // create 'copy' of axios instance

//     const [currentPage, setCurrentPage] = useState( <AxiosTestChild1/> )
    
//     return (
//         <div>
//         <button onClick={ function () {setCurrentPage(<AxiosTestChild1/>)}}>
//             Show List 1
//         </button>
//         <button onClick={ function () {setCurrentPage(<AxiosTestChild2/>)}}>
//             Show List 2
//         </button>
//         {currentPage}
//         </div>
//     );
// };

// export default AxiosTestMain;