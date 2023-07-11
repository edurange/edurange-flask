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

function InstructorView(props) {
    const [selectedStudent, setSelectedStudent] = useState();
    const [liveStuds, setLiveStuds] = useState();
    const [newMessage, setNewMessage] = useState(null);
    const [alert, setAlert] = useState();
    //const [instructID, setInstructID] = useState(uid);
   
 useEffect(() => {
  console.log("props.uid : " + props.uid)
  //console.log("uid : " + this.props.uid)
  
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
    let name = usernameList[i];
    let userID = (parseInt(i)+1).toString();
    let empty = []
    studentList.push({
      uid: userID,
      id: name,
      messages: empty
    });
  }

  socket.on("instructor session retrieval", (instructorPrevChat) => {
    for(let i in instructorPrevChat) {
      if(i!="000"){
        let previousChat = (instructorPrevChat[i] && instructorPrevChat[i].messages) ?
                        instructorPrevChat[i].messages :
                        [];
        studentList[parseInt(i)-2].messages = previousChat;
      }
    }
  });

  socket.on("new message", ({messageContents, _to, _from, room}) => {
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

  socket.on("live students", (masterLiveStuds) => {
    setLiveStuds(masterLiveStuds);
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
                    liveStuds={liveStuds}
                />
                <ChatWindow 
                    handleClick={handleClick} 
                    selectedStudent={selectedStudent}
                />
                  //fake dropdown
            <div class="dropdown">
              <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown">
            Dropdown button
              </button>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#">Link 1</a></li>
                <li><a class="dropdown-item" href="#">Link 2</a></li>
                <li><a class="dropdown-item" href="#">Link 3</a></li>
              </ul>
            </div>
            </div>

          
          
        );
}

var e = document.getElementById('instructor_view');
const root=createRoot(e);

root.render(<InstructorView uid={e.attributes.uid.value}/>);
