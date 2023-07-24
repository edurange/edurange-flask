import React, { useState, useEffect } from 'react';
import GroupChatWindow from '../group_chat_window/group_chat_window.component';

import HookTester from '../hook_tester/hook_tester';
import { io } from 'socket.io-client';
import "./group_client_socket.styles.css"

const socket = io(`${window.location.hostname}:3001`, {autoConnect: false});

// catch-all listener for development phase
socket.onAny((event, ...args) => {
  //console.log(event, args);
});

function GroupClientSocket(props) {
  const [inputData, setInputData] = useState("");
  const [messages, setMessages] = useState([]);
  const [val, setVal] = useState(0); 
  
  useEffect(() => {
    console.log(`SOCKET messages now: ${messages}}`)

    const uid = props.uid;
    const sid = props.sid;
    socket.auth = { uid, sid };
    socket.connect();
    
//group session retrieval, new group message, send group message

  // socket_event
    socket.on("group session retrieval", (prevChat) => {
      setMessages(prevChat);
    });

  // socket_event
    socket.on("new group message", ({messageContents, _from, _uname}) => {
      let newMessages = messages;
      let newMessage = {
        contents: messageContents,
        from: _from,
        uname: _uname,
        my_uid: props.uid,
      };
      newMessages.push(newMessage);
      setMessages(newMessages);
    });

    return () => {
      socket.off("group session retrieval");
      socket.off("new group message");
    };
    
  }, []);

  const onChange = (e) => {
    console.log("this is when we try to update");
    console.log(JSON.stringify(messages))
    setInputData(e.target.value);
  };

  const onFormSubmit = (e) => {
    //console.log("FORM SUBMIT")
    e.preventDefault();
    if (inputData) {
      console.log(inputData)
      socket.emit("send group message", {
        messageContents: inputData,
        _from: props.uid,
      });
      //console.log(JSON.stringify(messages))
      setInputData("");
    }
  };

  function printSomething() {
    console.log(`${JSON.stringify(messages)}`);
  }
  
  // Call the function every 2 seconds (2000 milliseconds)
  setInterval(printSomething, 2000);


  return (
    <div className="GroupClientSocket">
    <HookTester
      messages={messages}
    />
        <div className='chat-input-area'>
          <form onSubmit={onFormSubmit} autoComplete="off">
            <div className="input-group mb-3">
              <input
                type="text"
                className="form-control chat-input-box"
                autoComplete="off"
                onChange={onChange}
                value={inputData}
              />
              <button
                type="submit"
                className="btn btn-outline-success group_chat_send"
              >
                Send
              </button>
            </div>
          </form>
        </div>

    </div>
  );
}

export default GroupClientSocket;
