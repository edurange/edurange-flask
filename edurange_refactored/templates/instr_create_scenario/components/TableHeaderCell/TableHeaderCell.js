/* This is the entry point for the parent component page and
* the super container for the other components.
*/


// Corresponding stylesheet, in the same folder as the component. 
import "./TableHeaderCell.css";


import { createRoot } from 'react-dom/client';
import React, { useState, useEffect } from 'react';


// Your component should always begin with a capital letter.
function TableHeaderCell({ children }) {
       return (
              <th>{children}</th>
       );
}

export default TableHeaderCell;