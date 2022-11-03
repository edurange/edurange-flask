/* Display a student in the student_list. Attributes:
 * isEveryone - bool
 * hasNew - bool
 * studentName
 * currentScore
 */

import { useState, useEffect } from "react";
import "./student.css"

function Student(props) {
    var className = "list-group-item list-group-item-action d-flex justify-content-between"
    const [classNameState, setClassNameState] = useState(className);

    useEffect(() => {
        setClassNameState(`${className} ${props.status}`);
        if(props.selectedStudent==props.name) {
            setClassNameState(`${className} ${props.status} selected`);
        } else {
            setClassNameState(`${className} ${props.status}`);
        }
    },[props.status, props.selectedStudent]);

    const isLive = true;
    //
    if (!props.isLive) {
        className += " list-group-item-secondary"
    }
    return (
        <button 
            type="button" 
            id='student' 
            className={className} 
            onClick={() => props.onClick(props.name)}>
                {props.name}
                <div>
                {props.status == "unread" && 
                    <span>New</span>
                }
                </div>
        </button>
    );
}

export default Student;