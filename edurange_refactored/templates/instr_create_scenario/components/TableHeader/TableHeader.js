/* This is the entry point for the parent component page and
* the super container for the other components.
*/


// Corresponding stylesheet, in the same folder as the component. 
import "./TableHeader.css";
import TableRow from './TableRow';
import TableHeaderCell from './TableHeaderCell';

import { createRoot } from 'react-dom/client';
import React, { useState, useEffect } from 'react';


// Your component should always begin with a capital letter.
function TableHeader() {
       return (
              <thead className="thead-dark">
                     <TableRow>
                            <TableHeaderCell>Scenario</TableHeaderCell>
                            <TableHeaderCell>Description</TableHeaderCell>
                            <TableHeaderCell>Action</TableHeaderCell>
                     </TableRow>
              </thead>
       );
}


export default TableHeader;