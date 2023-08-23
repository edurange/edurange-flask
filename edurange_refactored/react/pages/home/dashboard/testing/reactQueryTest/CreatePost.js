

import React, {useState, useRef,useContext} from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { nanoid } from 'nanoid';
import QTList1 from './QTList1';
import QTList2 from './QTList2';


function CreatePost ({id}){

    function makePost (){
        return <>post made</>
    }
    
    const titleRef = useRef();
    const bodyRef = useRef(); 
    const createPostMutation = useMutation ({
        mutationFn:  makePost,
        onSuccess: (data, variables, context) =>{
            console.log(context)
        },
        onMutate: (variables) => {
            return {hi: "BYE!!"}

        },
        
          
    })
    function handleSubmit(event){
        event.preventDefault()
        createPostMutation.mutate({
            title: titleRef.current.value,
            body: bodyRef.current.value 

        }) 
    }
 
    return (
        <div>
            butt
        {/* {createPostMutation.isError && JSON.stringify(error)} */}
        <h1>Create Post</h1>
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="title">Title</label>
                <input id="title" ref={titleRef}/> 

            </div>
            <div>
                <label htmlFor="body">body</label>
                <input id="body" ref={bodyRef}/> 

            </div>
            <button disabled={createPostMutation.isLoading}>
                {createPostMutation ? "Loading..." : "Create"}
            </button>
        </form>
        </div>
    )
}

export default CreatePost;