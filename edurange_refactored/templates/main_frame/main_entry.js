import 'bootstrap/dist/css/bootstrap.css';
import  './../../../assets/css/pucs.css'
import  './../../../assets/css/style.css'
import React from 'react';
import { createRoot } from 'react-dom/client';
import MainFrame from './MainFrame';

const domNode = document.getElementById('root')
const root = createRoot(domNode);
root.render(<MainFrame/>)

