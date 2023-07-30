import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import "./socket_event_handler.styles.css"

import MessageWindow from '../message_window/message_window.component';"../message_window/message_window.component";
import EntryField from "../entry_field/entry_field.component";

const socket = io(`${window.location.hostname}:3001`, {autoconnect: false});
console.log(window.location.hostname)
// Testing Only:
// catch-all listener for development phase
socket.onAny((event, ...args) => {
    console.log(event, args);
  });

function SocketEventHandler(props) {

    const [instructorID, setInstructorID] = useState();
    const [instructorLive, setInstructorLive] = useState(false);
    const [messages, setMessages] = useState([]);

    useEffect( () => {
        const uid = props.uid;
        const sid = props.sid;
        const is_instructor = false;

        socket.auth = { uid, sid, is_instructor};
        socket.connect();
    }, [props.uid, props.sid]); // This hook is called when props passed. 


    useEffect( () => {

        socket.on("instructor live", ({instructorID}) => {
            setInstructorID(instructorID);
            setInstructorLive(true);
        });

        socket.on("new message", ({data}) => {
            setMessages([...messages, data]);
        });

        socket.on("instructor disconnected", () => {
            setInstructorLive(false);
        });

    }, []);
   

    const handleSendMessage = (message) => {
        socket.emit("send button pressed", {message});
    };
    
      return (
        <div>
          <MessageWindow messages={messages} uid={props.uid} />
          <EntryField onSendMessage={handleSendMessage} />
        </div>
      );
}

export default SocketEventHandler;