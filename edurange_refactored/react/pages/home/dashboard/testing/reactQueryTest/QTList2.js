
import React, {useContext} from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { nanoid } from 'nanoid';

const POSTS = [
    { id: 1, title: "Post 1"},
    { id: 2, title: "Post 2"}
]
function QTList2() {


    // queryKey examples (for multiple request arguments)
    //
    // /posts           ["posts"]
    // /posts/1         ["posts", "page"]
    // /posts/1/main    ["posts", "page", "section"]
    //

    const queryClient = useQueryClient();

    const postsQuery = useQuery({
        queryKey: ["somethingUnique"],
        queryFn: function (queryFnObj) {
            
            console.log(queryFnObj)
            return [...POSTS]

        }
    })

    const newPostMutation = useMutation ( {
        mutationFn: function (title) {
            POSTS.push ({ id: nanoid(5), title })
        },
        onSuccess: function() {
            queryClient.invalidateQueries(["somethingUnique"])
        }
    } )
    
    if (postsQuery.isLoading) {return <h1>Loading...</h1>}
    if (postsQuery.isError) {return <h1>Uh oh! {JSON.stringify(postsQuery.error)} </h1>}



    return (
        <div>
            {postsQuery.data.map(function (post) { 
                return (
                        <div key = {post.id}>
                            {post.title}
                        </div>
                )
            })}
        <button onClick={ function () {
            newPostMutation.mutate("new Post")
        }}>
            Add New
        </button>

        </div>
    )
}

export default QTList2;