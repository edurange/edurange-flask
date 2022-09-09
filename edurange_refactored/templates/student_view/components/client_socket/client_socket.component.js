import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('localhost:3001');

// catch-all listener for development phase
socket.onAny((event, ...args) => {
  console.log(event, args);
});

function ClientSocket() {
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [lastMessage, setLastMessage] = useState(null);
  const [inputData, setChange] = useState(null);

  useEffect(() => {
    socket.on('connect', () => {
      setIsConnected(true);
    });
    socket.on('disconnect', () => {
      setIsConnected(false);
    });
    socket.on('receive_message', data => {
      setLastMessage(data);
    });
    return () => {
      socket.off('connect');
      socket.off('disconnect');
      socket.off('message');
    };
  });

  const sendMessage = () => {
    socket.emit('message', inputData);
  }

  const onChange = (e) => {
    setChange(e.target.value);
  }

  return (
    <div className="ClientSocket">
      <header className="ClientSocket-header">
        <p>Connected: { '' + isConnected }</p>
        <p>Last message: { lastMessage || 'lastMessage' }</p>
        <p>Input Data: { inputData || 'inputData' }</p>
        <p>Socket: { socket.id }</p>
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


