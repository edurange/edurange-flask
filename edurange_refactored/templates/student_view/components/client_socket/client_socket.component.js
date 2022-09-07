/*
import io from 'socket.io-client';
import React, { useState, useEffect } from 'react';

const socket = io('localhost:3001');
function ClientSocket() {

  const [lastMessage, setLastMessage] = useState(null);
  
  
  return (
    <div>
      <button>APPPPPP</button>
    </div>
  );
}

export default ClientSocket;

*/
/*
//grabbing the port number from the .env file
require('dotenv').config({ path: '../../.env' })
*/
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('localhost:3001');

function ClientSocket() {
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [lastMessage, setLastMessage] = useState(null);

  useEffect(() => {
    socket.on('connect', () => {
      setIsConnected(true);
    });
    socket.on('disconnect', () => {
      setIsConnected(false);
    });
    // i before e
    // except after c
    // unless it makes the sound "a"
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
    socket.emit('hello!');
  }

  return (
    <div className="ClientSocket">
      <header className="ClientSocket-header">
        <div>
        <button>CLIENT SOCKET</button>
        </div>
        <p>Connected: { '' + isConnected }</p>
        <p>Last message: { lastMessage || 'you' }</p>
        <p>Socket: { socket.id }</p>
        <button onClick={ sendMessage }>Say hello!</button>
      </header>
    </div>
  );
}


export default ClientSocket;


