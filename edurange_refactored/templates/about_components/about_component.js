/* This is the entry point for the instructor view and 
 * the super container for the other components.
 */ 
import "./about_page.css";
import {createRoot} from 'react-dom/client';
import React, { useState, useEffect } from 'react';

function About(props) {
    // const [selectedStudent, setSelectedStudent] = useState();

  return (
        <div id="about_page">
    <h1 class="mt-5">About</h1>
        <div class="row">
            <p class="lead">Teaching cybersecurity or computer networking in the classroom? Our suite of exercises can help supplement your lectures, labs, and other activities. EDURange provides rapid feedback to students and faculty, aiding in the assessment of student learning. By providing interactive, competitive exercises, it enhances the quality of instructional material while increasing active learning for students.
            </p>
            </div>
        </div>
       
        );
}

var e = document.getElementById('about_page');
const root=createRoot(e);

root.render(<About/>);