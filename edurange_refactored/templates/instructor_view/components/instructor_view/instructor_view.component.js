/* This is the entry point for the instructor view and 
 * the super container for the other components.
 */ 
//import { io } from 'socket.io-client';
import Student from "../student/student.component";
import "./instructor_view.css";
import ChatWindow from "../chat_window/chat_window.component";
import StudentList from "../student_list/student_list.component";
import {createRoot} from 'react-dom/client';
import React, { useState, useEffect } from 'react';
function InstructorView() {
    const [input, setInput] = useState("chat");
    const [selectedUser, setSelectedUser] = useState();
    const [displayMessages, setDisplayMessages] = useState();

  const handleClick = (event, chatInput) => {
    console.log(event.target);

    setInput(chatInput);
  };

  const returnSelectedUser = (userObj) => {
    setSelectedUser(userObj);
    console.log(`instructor view userObj passed! : ${JSON.stringify(userObj)}`);
    setDisplayMessages(userObj["messages"]); //
  };



  
  return (

            <div id="instructor_view">
                <StudentList
                    returnSelectedUser={returnSelectedUser}
                />
                <ChatWindow 
                    handleClick={handleClick} 
                    selectedUserChat={displayMessages}
                />
            </div>
        );
}

var e = document.getElementById('instructor_view');
const root=createRoot(e);

root.render(<InstructorView />);

/*


function Child({handleClick}) {
  return (
    <div>
      <button onClick={event => handleClick(event, 100)}>
        Click
      </button>
    </div>
  );
}

export default function Parent() {
  


            <Student />
                <ChatWindow />

*/
