import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('localhost:3001');

// catch-all listener for development phase
socket.onAny((event, ...args) => {
  console.log(event, args);
});

function ClientSocket(props) {
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [lastMessage, setLastMessage] = useState(null);
  const [inputData, setChange] = useState(null);
  const [roomName, setRoomName] = useState(null);
  const [socketUserID, setSocketUserID] = useState(null);
  const [socketInstructorStatus, setSocketInstructorStatus] = useState(socket.isInstructor)

  useEffect(() => {
    socket.on('connect', () => {
      setIsConnected(true);
      setSocketInstructorStatus(false);
    });
    socket.on('disconnect', () => {
      setIsConnected(false);
    });
    socket.on('message', data => {
      setLastMessage(data);
    });

    socket.on('room_joined', roomNameData => {
      setRoomName(roomNameData);
    });

    const sessionID = localStorage.getItem("sessionID");
 
    if (sessionID) {
      socket.auth = { sessionID };
      socket.connect();
    }
  
    socket.on("session", ({ sessionID, userID, isInstructor }) => {
      // attach the session ID to the next reconnection attempts
      socket.auth = { sessionID };
      // store it in the localStorage
      localStorage.setItem("sessionID", sessionID);
      // save the ID of the user
      socket.userID = userID;
      // save the instructor status of the user
      socket.isInstructor = isInstructor;
    });

    socket.on('private_message', ({content, from, to }) => {
      if (user.userID === (fromSelf ? to : from)) {
        user.messages.push({
          content,
          fromSelf,
        });
      }
    });

    return () => {
      socket.off('connect');
      socket.off('disconnect');
      socket.off('message');
    };
  });

  const sendMessage = () => {
    socket.emit('message', inputData);
    socket.emit('private_message', inputData);
  }

  const onChange = (e) => {
    setChange(e.target.value);
  }

  

  return (
    <div className="ClientSocket">
      <header className="ClientSocket-header">
        <p>USER ID: {props.uid}</p>
        <p>Connected: { '' + isConnected }</p>
        <p>Room name: { roomName } </p>
        <p>Last message: { lastMessage || 'lastMessage' }</p>
        <p>Input Data: { inputData || 'inputData' }</p>
        <p>Socket: { socket.id }</p>
        <p>isInstructor: { socketInstructorStatus }</p>

        <div className='chat-input-area'>
            <form
              onSubmit={ sendMessage }
              autoComplete="off"
            >
            <input
              type='text'
              className="chat-input-box"
              onChange={ onChange }
              />
            </form>
            </div>
        <button onClick={ sendMessage }>Say hello!</button>
      </header>
    </div>
  );
}


export default ClientSocket;


