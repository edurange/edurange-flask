// Filename: student_veiw.js
import "./student_veiw.css";
import {createRoot} from 'react-dom/client';
import React, { useState, useEffect } from 'react';

function Student(props) {
    // const [selectedStudent, setSelectedStudent] = useState();

    return (
<div id="student_veiw"> 
    <h1 class="mt-5">Student</h1>

{% extends "layout.html" %}
{% block content %}
    <link
            rel="stylesheet"
            type="text/css"
            href="{{ url_for('static', filename='build/student_scenario.bundle.css') }}"
    />
<main class="student">
  <div id="student_scenario" scenario_id={{scenario_id}}></div>
</div>
</main>

{% endblock %}

{% block  js %}
<!-- development React scripts !!Replace with production scripts (below) for release!! -->
<!-- script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script
<script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script> -->

<!-- production React scripts -->
<!-- <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script> -->

<script src="/static/build/student_scenario.bundle.js"></script>
{% endblock %}

</div>
    );
}   
var e = document.getElementById('student_veiw');
const root=createRoot(e);

root.render(<About/>);