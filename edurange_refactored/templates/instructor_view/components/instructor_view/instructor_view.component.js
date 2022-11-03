/* This is the entry point for the instructor view and 
 * the super container for the other components.
 */ 
//import { io } from 'socket.io-client';
import Student from "../student/student.component";
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
 
var allStudents = [];
var global_msg_list=[];
var newest_msg = "";

function InstructorView() {
    //const [displayMessages, setDisplayMessages] = useState(null);
    const [currAlert, setCurrAlert] = useState();
    const [selectedStudent, setSelectedStudent] = useState();
    const [newMessage, setNewMessage] = useState(null);
    const [alert, setAlert] = useState();
    const usernames = usernameList;
   
 
 useEffect(() => {
  const uid = "000";
  socket.auth = { uid } // .auth : uid sent during client-request in TCP handshake.
  socket.connect();

  socket.on('connect', () => {
    console.log("instructor has connected.");
  });
  socket.emit("instructor connected");

  // Alerts (message, join, and leave) passed to StudentList component.
  socket.on("alert", (_alert) => {
     
      //NEED TO FIX ---- ALERT SHOULD ALREADY HAVE ID AND TIME
      _alert["id"] = usernames[_alert["uid"] - 1]; // user1 has a uid of 2.
      _alert["time"] = new Date().toISOString()
        .replace('T', ' ')
        .replace('Z', ''); // user1 has a uid of 2.
      
      //NEED TO FIX --- MAKE ACTIVE LIST INSTEAD OF ALL STUDENTS
      allStudents.push(_alert);
      setAlert(_alert);
      //onRecvAlert(_alert);
  });

  socket.on("new message", ({messageContents, _to, _from, room}) => {
      socket.emit("request msg_list", {messageContents, _to, _from, room});
  });

  socket.on("msg_list update", ({msg_list, room}) => {
    for(let i in allStudents) {
      if (allStudents[i]["uid"] == room) {
        allStudents[i]["messages"] = msg_list;
        setNewMessage(msg_list); // by changing a state, the component is forced to update. 
      }
    }
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
        _from: "000"
      });
    } else if (chatInput && !selectedStudent) {
      console.log("chatInput data, no selectedStudent");
    }
  };
  
  // this handler function is passed to student list
  const returnSelectedUser = (displayName) => {  
    for(let i = 0; i < allStudents.length; i++){
      if (allStudents[i]["id"] == displayName) {
        setSelectedStudent(allStudents[i]);
      }
    }
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
