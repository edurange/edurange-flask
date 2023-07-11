import React, { Component, useEffect } from 'react';
import './student_veiw.css';

function Student({ scenario_id }){
    useEffect(() => {
        //script
        const script = document.createElement('script');
        script src="/static/build/student_scenario.bundle.js";
        script.async = true;
        document.body.appendChild(script);

        return () => {
            document.body.removeChild(script);
        };
    }, []);
    return (
        <div>
            <link rel="stylesheet" href="/static/build/student_scenario.css" />
            /&gt;
            <main className='student'>
                <div id="student_scenario" scenario_id={scenario_id}></div>
            </main>
        </div>
    );
}
export default Student;
import React from 'react';
import Student from './student_veiw.js';

function App() {
    return <div>
        <Student scenario_id={scenario_id} />
        <Student scenario_id="123"/>
       
        </div>
    
}
var e = document.getElementById('student_veiw');
const root=createRoot(e);

root.render(<Student/>);