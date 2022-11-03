import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

const socket = io(`${window.location.hostname}:3001`, {autoConnect: false});

// catch-all listener for development phase
socket.onAny((event, ...args) => {
  console.log(event, args);
});

function ClientSocket(props) {
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [inputData, setInputData] = useState("");
  
  useEffect(() => {
    const uid = props.uid;
    socket.auth = { uid };
    socket.connect();

    socket.on("connect", () => {
      console.log(`Student with ID '${uid}' is connected!`);
    });

    socket.on("new message", ({messageContents, _to, _from, room}) => {
      socket.emit("request msg_list", {messageContents, _to, _from, room});
  });


  socket.on("msg_list update", (msg_list) => {
    console.log(`STUDENT: message is ${JSON.stringify(msg_list)}`);
});


    const listener = event => {
      if (event.code === "Enter" || event.code === "NumpadEnter") {
        event.preventDefault();
        if(inputData) {
          socket.emit("send message", {messageContents: inputData, _to: "instructor", _from: uid});
          setInputData("");
        }
      }
    };

    document.addEventListener("keydown", listener);

    return () => {
      socket.off('connect');
      socket.off("new message");
      socket.off("send message");
      socket.off("msg_list update");
      document.removeEventListener("keydown", listener);
    };

  });

  const onChange = (e) => {
    setInputData(e.target.value);
  }

  const onFormSubmit = e => {
    e.preventDefault();
    if(inputData) {
        socket.emit("send message", {messageContents: inputData, _to: "000", _from: props.uid});
        setInputData("");
    }
  }


  return (
    <div className="ClientSocket">
    <StudentChatWindow chat_opened={props.chat_opened}/>
        <p>Connected: { '' + isConnected }</p>

        <div className='chat-input-area'>
            <form
              onSubmit={ onFormSubmit }
              autoComplete="off"
            >
              <input
                type='text'
                className="chat-input-box"
                autoComplete='off'
                onChange={ onChange }
                value= {inputData}
              />
              <button
                type="submit"
              >
              Send
              </button>

            </form>
        </div>

    </div>
  );
}

export default ClientSocket;


