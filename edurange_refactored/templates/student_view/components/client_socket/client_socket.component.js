import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io(`${window.location.hostname}:3001`);

// catch-all listener for development phase
socket.onAny((event, ...args) => {
  console.log(event, args);
});

function ClientSocket(props) {
  const [isConnected, setIsConnected] = useState(socket.connected);

  useEffect(() => {
    socket.on('connect', () => {
      setIsConnected(true);
      socket.emit("student connected", props.uid);
      //emit props.
    });

    const sessionID = localStorage.getItem("sessionID");

    return () => {
      socket.off('connect');
    };
  });

  /* TO DO MESSAGE.
  const sendMessage = () => {
    socket.emit('message', inputData);

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
  }*/

  const onChange = (e) => {
    setChange(e.target.value);
  }

  

  return (
    <div className="ClientSocket">
        <p>Connected: { '' + isConnected }</p>
    </div>
  );
}

export default ClientSocket;


