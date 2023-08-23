 

import React, {useState, useContext} from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { nanoid } from 'nanoid';
import QTList1 from './QTList1';
import QTList2 from './QTList2';


function QTPost ({id}){
    const postQuery = useQuery({
        queryKey: ['posts',id],
        queryFn: function(){
            console.log("making API request!")
        }
    })
 
    return (
        <div>
        <button onClick={ function () {setCurrentPage(<QTList1/>)}}>
            Show List 1
        </button>
        <button onClick={ function () {setCurrentPage(<QTList2/>)}}>
            Show List 2
        </button>
        {currentPage}
        </div>
    )
}

export default QTPost;