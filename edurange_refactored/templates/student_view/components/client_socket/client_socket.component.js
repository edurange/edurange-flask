//import React BREAK
//import React, { useState, useEffect } from 'react';

//importing io BREAK
//import io from 'socket.io-client';

/*
class ClientSocket extends React.Component {
  render() {
    return (
      <div>
        <button>APPPPPP</button>
      </div>
    );
  }
}
*/

function ClientSocket() {
  return (
    <div>
      <button>APPPPPP</button>
    </div>
  );
}

export default ClientSocket;
/*
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('localhost:3001');

function App() {
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [lastMessage, setLastMessage] = useState(null);

  useEffect(() => {
    socket.on('connect', () => {
      setIsConnected(true);
    });
    socket.on('disconnect', () => {
      setIsConnected(false);
    });
    socket.on('message', data => {
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
    <div className="App">
      <header className="App-header">
        <p>Connected: { '' + isConnected }</p>
        <p>Last message: { lastMessage || '-' }</p>
        <button onClick={ sendMessage }>Say hello!</button>
      </header>
    </div>
  );
}
*/

