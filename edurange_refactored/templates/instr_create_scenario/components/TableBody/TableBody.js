/* This is the entry point for the parent component page and
* the super container for the other components.
*/


// Corresponding stylesheet, in the same folder as the component. 
import "./TableBody.css";
import TableRow from './TableRow';
import TableCell from './TableCell';
import Button from './Button';

import { createRoot } from 'react-dom/client';
import React, { useState, useEffect } from 'react';


// Your component should always begin with a capital letter.
function TableBody({ scenarios }) {
       return (
              <tbody>
                     {scenarios.map((s) => (
                            <TableRow key={s.name}>
                                   <TableCell>{s.name}</TableCell>
                                   <TableCell>{s.description}</TableCell>
                                   <TableCell>
                                          <Button label="Create" />
                                   </TableCell>
                            </TableRow>
                     ))}
              </tbody>
       );
}


export default TableBody;