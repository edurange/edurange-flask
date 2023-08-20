
import "../demo.css"
import React from 'react';

// functional component as opposed to class component
function Parent() {



    // most React components return JSX, which is React's version of HTML
    // and is usually what is rendered when the component is evaluated
    return (
        <>
            
        </>
    )

}
export default Parent;
// you need to export your component or it can't be used by other components
// the 'default' keyword means that when you import this component, 
// if no function is specified, it will use the default function (which is this whole component)