/* This is the entry point for the parent component page and
* the super container for the other components.
*/


// Corresponding stylesheet, in the same folder as the component. 
import "./accountmgmt.css";


import {createRoot} from 'react-dom/client';
import React, { useState, useEffect } from 'react';


// Your component should always begin with a capital letter.
function Accountmgmt(props) {
 return (
           <div id="accountmgmt">
    <h1>Parent Component Successfully Rendered!</h1>
           </div>
       );
}


var e = document.getElementById("accountmgmt"); // The id assigned in html file. 
const root=createRoot(e);


root.render(<Accountmgmt/>);



