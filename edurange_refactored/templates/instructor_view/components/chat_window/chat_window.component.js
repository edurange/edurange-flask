/* Display one chat session.
 */

import "./chat_window.css"
import React, { useState, useEffect } from 'react';
import ChatEntry from "../chat_entry/chat_entry.component";
//import ChatInput from "../chat_input/chat_input.component";



function ChatWindow({handleClick, selectedStudent}) {
    const [user, setUser] = useState("");  
    const [input, setInput] = useState("");                      //Current user
    const [messages, setMessages] = useState(null);
    const chat = React.createRef();   
    
    useEffect(()=>{
        if(selectedStudent) {
            setUser(selectedStudent);
        }

        const listener = event => {
            if (event.code === "Enter" || event.code === "NumpadEnter") {
              if(input) {
                event.preventDefault();
                handleClick(event, input);
                setInput("");
              }
            }
          };
      
        document.addEventListener("keydown", listener);

        return () => {
            document.removeEventListener("keydown", listener);
        };
    }, [selectedStudent]);                       //Input entry for chat

    function getMessagesContent(selectedStudent) {  

        if(selectedStudent && selectedStudent["messages"]) { 
            let studentID = selectedStudent["id"];
            let messageList = selectedStudent["messages"].map((message) =>             //Map the messages to a component
                <ChatEntry key={Math.random() * 100} 
                message={message.contents} 
                fromSelf={message.from=="000"} 
                user={message.from=="000"?"me":studentID} 
                />
            )
            return messageList; 
        }                                    //Return the componenet for rendering
        return;
    }

    function onSubmit(e) {                                        //Send input as a chat message
        e.preventDefault();
        handleClick(e, input); 
        setInput("");//Clear current message from input      
    }

    const onChange = (e) => {
        setInput(e.target.value);
    }

    
    
    return(
         <div id='chatWindow'>
          {getMessagesContent(selectedStudent)}
            {/* Render the current messages */}
            {/* <ChatInput /> */}                                   
            <div id='chat_input'>
                {/* Input component */}

                {selectedStudent && <form onSubmit={onSubmit} autoComplete="off" id="chat_entry_box" >
                    <input 
                        type='text'
                        placeholder="Your Text Here!"
                        onChange={onChange}
                        value= {input} 
                        ref={chat}
                        className="chat_input_area" 
                        />
                    <button className='edu-submit' type="submit">
                        Send
                    </button>
                </form>}
            </div>
        </div>
    );
}

export default ChatWindow;