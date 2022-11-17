/* This is the entry point for the instructor view and 
 * the super container for the other components.
 */ 
import "./instructor_view.css";

import ChatWindow from "../chat_window/chat_window.component";
import StudentList from "../student_list/student_list.component";
import usernameList from '../../../../../../edurange-flask/data/tmp/chatnames.json'

import {createRoot} from 'react-dom/client';
import React, { useState, useEffect } from 'react';

import { io } from 'socket.io-client';
const socket = io(`${window.location.hostname}:3001`, {autoConnect:false}); //autoconnect false. Connection once uid sent.
 
// catch-all listener for development phase
socket.onAny((event, ...args) => {
 console.log(event, args);
});
 
let studentList = [];

function InstructorView() {
    const [selectedStudent, setSelectedStudent] = useState();
    const [newMessage, setNewMessage] = useState(null);
    const [alert, setAlert] = useState();
   
 useEffect(() => {
  const uid = "000";
  socket.auth = { uid } // .auth : uid sent during client-request in TCP handshake.
  socket.connect();

  socket.on('connect', () => {
    console.log("instructor has connected.");
  });

  // Alerts (message, join, and leave) passed to StudentList component.
  socket.on("alert", (_alert) => {
    _alert.connected = _alert.type=="studLeave" ? false : true;
    setAlert(_alert);
  });

  for(let i in usernameList) {
    console.log(`i ${i}`)
    let name = usernameList[i];
    let userID = (parseInt(i)+1).toString();
    let empty = []
    studentList.push({
      uid: userID,
      id: name,
      messages: empty
    });
    console.log(`i ${i} JSONstudentList ${JSON.stringify(studentList[i])}`)
  }

  socket.on("instructor session retrieval", (instructorPrevChat) => {
    for(let i in instructorPrevChat) {
      if(i!="000"){
        let previousChat = (instructorPrevChat[i] && instructorPrevChat[i].messages) ?
                        instructorPrevChat[i].messages :
                        [];
        //console.log(`studentList[parseInt(i)-2] ${JSON.stringify(studentList[parseInt(i)-2])}`)
        studentList[parseInt(i)-2].messages = previousChat;
        
        //console.log(`studentList[parseInt(i)-2] ${JSON.stringify(studentList[parseInt(i)-2])}`)
      }
    }
  });

  socket.on("new message", ({messageContents, _to, _from, room}) => {
    //console.log(`request message recieved : ${messageContents} to ${_to} from ${_from}`)
    let newMessage = {
      contents: messageContents,
      to: _to,
      from: _from,
    };
    let student = studentList.find(student => student.uid == room)
    let tmpMessages = student.messages;
    tmpMessages.push(newMessage);
    student.messages = tmpMessages;
    
    setNewMessage(newMessage); // changing the value of some state forces the component to update
  });

   return () => {
      // cleanup sockets when component "dismounts"
      socket.off('connect');
      socket.off('alert');
      socket.off('new message');
      socket.off('msg_list update');
    };
  }, []);
  
    const handleClick = (event, chatInput) => {
    if(chatInput && selectedStudent) {
      socket.emit("send message", {
        messageContents: chatInput,
        _to: selectedStudent["uid"],
        _from: "000",
      });
    } else if (chatInput && !selectedStudent) {
      console.log("chatInput data, no selectedStudent");
    }
  };
  
  // this handler function is passed to student list
  const returnSelectedUser = (displayName) => {
    console.log("Instructor view: Selected student" + JSON.stringify(displayName));
    console.log("Student List to select students:");
    console.log(JSON.stringify(studentList))
    setSelectedStudent(studentList.find(student => student.id == displayName));
  };

  return (
            <div id="instructor_view">
                <StudentList
                    returnSelectedUser={returnSelectedUser}
                    alert={alert}
                />
                <ChatWindow 
                    handleClick={handleClick} 
                    selectedStudent={selectedStudent}
                />
            </div>
        );
}

var e = document.getElementById('instructor_view');
const root=createRoot(e);

root.render(<InstructorView />);
