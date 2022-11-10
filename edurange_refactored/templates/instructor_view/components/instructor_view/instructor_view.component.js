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
 
var studentList = [];

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
    
    // assign or retrieve master "studentList"
    if(window.localStorage.getItem("allStudentMessages")) {
      studentList = JSON.parse(window.localStorage.getItem("allStudentMessages"));
    } else {
      for(let i in Object.values(usernameList)) {
        studentList.push({
          messages: [],
          uid:(parseInt(i)+2).toString(),
          id: Object.values(usernameList)[i], 
          connected: false,
        });
      }
    }
  });

  // Alerts (message, join, and leave) passed to StudentList component.
  socket.on("alert", (_alert) => {
    //let alertStud = studentList[parseInt(_alert["uid"])-2];
    _alert.connected = _alert.type=="studLeave" ? false : true;
    console.log(`ALERT: ${JSON.stringify(_alert)}`);
    setAlert(_alert);
  });

  socket.on("instructor previous chat", (instructorPrevChat) => {
    for(let i in instructorPrevChat) {
      if(i!="000"){
        studentList[parseInt(i)-2]["messages"] = instructorPrevChat[i]["messages"];
        console.log(`studentList[parseInt(i or ${i})-2]["messages"] :: ${JSON.stringify(studentList[parseInt(i)-2]["messages"])}`)
      }
      
      console.log(JSON.stringify(i));
      console.log(`type of i ${typeof i}`);
    }
  });

  socket.on("new message", ({messageContents, _to, _from, room}) => {
    socket.emit("request msg_list", {messageContents, _to, _from, room});
  });

  socket.on("msg_list update", ({msg_list, room}) => {
    studentList[parseInt(room)-2]["messages"] = msg_list;
    setNewMessage(msg_list); // changing the value of some state forces the component to update
    
    console.log("PERSISTING MESSAGES " + JSON.stringify(studentList) );
    //persist messages.
    window.localStorage.setItem('allStudentMessages', JSON.stringify(studentList));
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
