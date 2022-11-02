/* Display one chat session.
 */

import "./chat_window.css"
import React, { useState, useEffect } from 'react';
import ChatEntry from "../chat_entry/chat_entry.component";
//import ChatInput from "../chat_input/chat_input.component";



function ChatWindow({handleClick, displayMessages}) {
    const [user, setUser] = useState("");  
    const [input, setInput] = useState("");                      //Current user
    const [messages, setMessages] = useState(null);
    const chat = React.createRef();   
    
    useEffect(()=>{
        if(displayMessages) {
            setMessages(displayMessages);

        }
      
     }, [displayMessages]);                       //Input entry for chat

    // useEffect(() => {
    //         setMessages([
    //             ...messages,
    //             {
    //                 fromSelf: true,
    //                 content: {data},
    //                 id: "You",
    //             }
    //         ]);
    //     });
    // });

    function getMessagesContent(displayMessages) {                         
        if(displayMessages && displayMessages.length != 0) {  
            let studentID = (displayMessages[0].from=="000") ? displayMessages[0].to : displayMessages[0].from; 
            let messageList = displayMessages.map((message) =>             //Map the messages to a component
                <ChatEntry key={Math.random() * 100} 
                message={message.contents} 
                fromSelf={message.from=="000"} 
                user={studentID} 
                />
            )
            return messageList;                                     //Return the componenet for rendering
        } else if(!displayMessages) { 
            console.log("CHAT WINDOW NO DISPLAY MESSAGES");
        }

    return;
    }

    function onSubmit(e) {  
        console.log("on submit reached.")                                        //Send input as a chat message
        e.preventDefault();
        /*                                         //Don't refresh the whole page when a message is sent
        setMessages([...messages,                                   //Add new message to message list
            {
                fromSelf: true,
                content: chat.current.value,
                user: "Me",
            }]);
            */
        setInput("");//Clear current message from input  
        handleClick(e, input);     
    }

    const onChange = (e) => {
        setInput(e.target.value);
        console.log(input);
    }
    
    return(
         <div id='chatWindow'>
          {getMessagesContent(displayMessages)}
                                      {/* Render the current messages */}
            {/* <ChatInput /> */}                                   {/* Input component */}
            <div id='chat_input'>
                <form onSubmit={onSubmit} autoComplete="off" id="chat_entry_box" >
                    <input 
                        type='text'
                        placeholder="Your Text Here!"
                        onChange={ onChange }
                        value= {input} 
                        ref={chat}
                        className="chat_input_area" 

                        />
                    <button className='edu-submit' type="submit">
                        Send
                    </button>
                    
                </form>
            </div>
        </div>
    );
}

export default ChatWindow;