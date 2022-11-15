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

  socket.on("instructor session retrieval", (instructorPrevChat) => {
    for(let i in instructorPrevChat) {
      if(i!="000"){
        if(instructorPrevChat[i] && instructorPrevChat[i].messages) {
          console.log(`instructorPrevChat                             : ${JSON.stringify(instructorPrevChat)}`)
          console.log(`instructorPrevChat[i]                          : ${instructorPrevChat[i]}`)
          console.log(`instructorPrevChat[i].messages              : ${instructorPrevChat[i].messages}`)
          console.log(`studentList                             : ${JSON.stringify(studentList)}`)
          console.log(`studentList[parseInt(i)-2]              : ${studentList[parseInt(i)-2]}`)
          studentList[parseInt(i)-2] = {
            messages: instructorPrevChat[i].messages
          }
        } else {
          studentList[parseInt(i)-2] = {
            messages = []
          }
        }
      }
    }
  });

  socket.on("new message", ({messageContents, _to, _from, room}) => {
    console.log(`request message recieved : ${messageContents} to ${_to} from ${_from}`)
    let newMessage = {
      contents: messageContents,
      to: _to,
      from: _from,
    };
    if(!studentList[parseInt(room)-2].messages) {
      studentList[parseInt(room)-2].messages = [];
    }
    let tmpMessages = studentList[parseInt(room)-2].messages;
    tmpMessages.push(newMessage);
    studentList[parseInt(room)-2].messages = tmpMessages;
    
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
