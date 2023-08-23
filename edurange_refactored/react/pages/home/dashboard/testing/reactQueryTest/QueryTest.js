
import React, {useState, useContext} from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { nanoid } from 'nanoid';
import QTList1 from './QTList1';
import QTList2 from './QTList2';
import CreatePost from './CreatePost';

function QueryTest() {

    const [currentPage, setCurrentPage] = useState(<QTList1/>)
    
    return (
        <div>
        <button onClick={ function () {setCurrentPage(<QTList1/>)}}>
            Show List 1
        </button>
        <button onClick={ function () {setCurrentPage(<QTList2/>)}}>
            Show List 2
        </button>
        {currentPage}
        <CreatePost/>
        </div>
    )
}

export default QueryTest;