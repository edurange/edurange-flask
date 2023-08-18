/* This is the entry point for the parent component page and
* the super container for the other components.
*/


// Corresponding stylesheet, in the same folder as the component. 
import "./parent_component.css";


import {createRoot} from 'react-dom/client';
import React, { useState, useEffect } from 'react';


// Your component should always begin with a capital letter.
function ParentComponent(props) {
 return (
           <div id="parentComponent">
    <h1>ParentComponent Successfully Rendered!</h1>
           </div>
       );
}


var e = document.getElementById(‘parentComponent’); // The id assigned in html file. 
const root=createRoot(e);


root.render(<ParentComponent/>);