/* This is the entry point for the instructor view and 
 * the super container for the other components.
 */ 
import io from 'socket.io-client';
import Student from "../student/student.component";
import "./instructor_view.css";
import ChatWindow from "../chat_window/chat_window.component";
import StudentList from "../student_list/student_list.component";
import {createRoot} from 'react-dom/client';
import React from 'react';
import chatnameMap from "../../../../../data/tmp/chatnames.json";

/*
//TEMP ====================================
console.log("about to call socket io");
//const socket = io(`${window.location.hostname}:3001`);
const socket = io("localhost:3001");
//TEMP ====================================
console.log("after calling socket io");

// catch-all listener for development phase
socket.onAny((event, ...args) => {
  console.log(event, args);
});
*/

class InstructorView extends React.Component {
    constructor() {
        super();
        this.state = {
          usersList: [],
          selectedUser: null,
        };
      }

    componentDidMount() {
    }

    render() {
        
        return (

            <div id="instructor_view">
                <StudentList />
                <ChatWindow />
            </div>
        );
    }
}



var e = document.getElementById('instructor_view');
const root=createRoot(e);

root.render(<InstructorView />);

/*

            <Student />
                <ChatWindow />

*/
