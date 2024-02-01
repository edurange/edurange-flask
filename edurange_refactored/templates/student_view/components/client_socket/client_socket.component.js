import React, { useState, useEffect } from 'react';
import StudentChatWindow from '../student_chat_window/student_chat_window.component';
import { io } from 'socket.io-client';
import "./client_socket.styles.css"

const socket = io(`${window.location.hostname}:3001`, {autoConnect: false});

// catch-all listener for development phase
socket.onAny((event, ...args) => {
  console.log(event, args);
});

function ClientSocket(props) {
  const [inputData, setInputData] = useState("");
  const [messages, setMessages] = useState();
  const [val, useVal] = useState(0); 
  
  useEffect(() => {
    const uid = props.uid;
    const sid = props.sid;
    socket.auth = { uid, sid };
    socket.connect();
    
    socket.on("student session retrieval", (prevChat) => {
      setMessages(prevChat);
    });

    socket.on("new message", ({messageContents, _to, _from, room}) => {
      let newMessages = messages ? messages : [];
      let newMessage = {
        contents: messageContents,
        to: _to,
        from: _from,
      };
      newMessages.push(newMessage);
      console.log("new message! messages now:: : " + JSON.stringify(messages));
      setMessages(newMessages);
      
    });

    /*
    socket.on("instructor connected", () => {
      socket.emit("student live");
    })
    */

    const listener = event => {
      if (event.code === "Enter" || event.code === "NumpadEnter") {
        
        console.log("enter pressed! messages now : " + JSON.stringify(messages));
        if(inputData) {
          setVal(val = val + 1); 
         
          /*
          event.preventDefault();
          socket.emit("send message", {messageContents: inputData, _to: "000", _from: uid});
          setInputData("");
          */
         onFormSubmit(event);
          
        }
      }
    };

    document.addEventListener("keydown", listener);

    return () => {
      socket.off("student session retrieval");
      socket.off("new message");
      document.removeEventListener("keydown", listener);
    };

  }, [messages]);

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
    <StudentChatWindow 
    
      chat_opened={props.chat_opened}
      messages={messages}  
      />

        <div className='chat-input-area'>
            <form
              onSubmit={ onFormSubmit }
              autoComplete="off"
            >
            <div className="input-group mb-3">
              <input
                type='text'
                className="form-control chat-input-box"
                autoComplete='off'
                onChange={ onChange }
                value= {inputData}
              />
              <button
                type="submit"
                className="btn btn-outline-success student_chat_send"
              >
              Send
              </button>
            </div>

            </form>
        </div>

    </div>
  );
}

export default ClientSocket;
