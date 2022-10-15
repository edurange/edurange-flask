/* This is the entry point for the instructor view and 
 * the super container for the other components.
 */ 
import io from 'socket.io-client';
//import Student from "../student/student.component";
import "./instructor_view.css";
//import ChatWindow from "../chat_window/chat_window.component";
import {createRoot} from 'react-dom/client';
import React, { useState, useEffect } from 'react';
import chatnameMap from "../../../../../data/tmp/chatnames.json";

//TEMP ====================================
console.log("about to call socket io");
const socket = io(`${window.location.hostname}:3001`);
//TEMP ====================================
console.log("after calling socket io");

// catch-all listener for development phase
socket.onAny((event, ...args) => {
  console.log(event, args);
});



function InstructorView() {

    const[studentList, setStudentList] = useState(null);

    var users;
    var selectedUser = null;

    useEffect(() => {
        socket.on("session", ({ sessionID, userID }) => {
            // attach the session ID to the next reconnection attempts
            socket.auth = { sessionID };
            // store it in the localStorage
            localStorage.setItem("sessionID", sessionID);
            // save the ID of the user
            socket.userID = userID;
          });
        
          socket.on("users", (users) => {
           //========TEMP ERROR CATCHER==========
            console.log("socket.on.users");
            setStudentList(users);
            users.forEach((user) => {
              console.log("for each user");
              user.messages.forEach((message) => {
                message.fromSelf = message.from === socket.userID;
              });
              for (let i = 0; i < this.users.length; i++) {
                const existingUser = this.users[i];
                if (existingUser.userID === user.userID) {
                  console.log("existing user ID == user ID");
                  //existingUser.connected = user.connected;
                  existingUser.messages = user.messages;
                  return;
                }
              }
              console.log("set user ID to socket user ID");
              user.self = user.userID === socket.userID;
              //initReactiveProperties(user);
              this.users.push(user);
            });
            // put the current user first, and sort by username
            console.log("sort user")
            this.users.sort((a, b) => {
              if (a.self) return -1;
              if (b.self) return 1;
              if (a.username < b.username) return -1;
              return a.username > b.username ? 1 : 0;
            });
          });
        
          socket.on("user connected", (user) => {
            //========TEMP ERROR CATCHER==========
            console.log("socket.on.user connected");
            for (let i = 0; i < this.users.length; i++) {
              const existingUser = this.users[i];
              if (existingUser.userID === user.userID) {
                //existingUser.connected = true;
                return;
              }
            }
            //initReactiveProperties(user);
            this.users.push(user);
          });

          
        
          socket.on("message", ({ content, from, to }) => {
            for (let i = 0; i < this.users.length; i++) {
            //========TEMP ERROR CATCHER==========
            console.log("socket.on.message");
              const user = this.users[i];
              const fromSelf = socket.userID === from;
              if (user.userID === (fromSelf ? to : from)) {
                user.messages.push({
                  content,
                  fromSelf,
                });
                if (user !== this.selectedUser) {
                  user.hasNewMessages = true;
                }
                break;
              }
            }
          });

          

          
    });
    
        
        return (

            <div id="instructor_view">
                
    
            </div>
        );
}

var e = document.getElementById('instructor_view');
const root=createRoot(e);

root.render(<InstructorView />);

/*

            <Student />
                <ChatWindow />

*/


