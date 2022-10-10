/* Display one chat session.
 */
import io from 'socket.io-client';
import "./chat_window.css"
import React, { useState, useEffect } from 'react';
import ChatEntry from "../chat_entry/chat_entry.component";
//import ChatInput from "../chat_input/chat_input.component";

const socket = io('localhost:3001');

function ChatWindow(props) {
    const [user, setUser] = useState(props);                        //Current user
    const [messages, setMessages] = useState([{                     //Messages for current user
        fromSelf: true,
        content: "Hello",
        user: "Me"
    },
    {
        fromSelf: false,
        content: "Hi",
        user: "You"
    }]);
    const chat = React.createRef();                          //Input entry for chat

    // useEffect(() => {
    //     socket.on('message', data => {
    //         setMessages([
    //             ...messages,
    //             {
    //                 fromSelf: true,
    //                 content: {data},
    //                 user: "You",
    //             }
    //         ]);
    //     });
    // });

    function getMessagesContent(messages) {                         //Get chat messages from server-side
        if(messages.length != 0){                                   //Ensure messages is an array
            let messageList = messages.map((message) =>             //Map the messages to a component
                <ChatEntry key={Math.random() * 100} message={message.content} fromSelf={message.fromSelf} user={message.user} />
            )
            return messageList;                                     //Return the componenet for rendering
        }
        return;
    }

    function onSubmit(e) {                                          //Send input as a chat message
        e.preventDefault();                                         //Don't refresh the whole page when a message is sent
        setMessages([...messages,                                   //Add new message to message list
            {
                fromSelf: true,
                content: chat.current.value,
                user: "Me",
            }]);
            document.getElementById("chat_entry_box").reset()       //Clear current message from input
    }
    
    return(
         <div id='chatWindow'>
            {getMessagesContent(messages)}                          {/* Render the current messages */}
            {/* <ChatInput /> */}                                   {/* Input component */}
            <div id='chat_input'>
                <form onSubmit={onSubmit} autoComplete="off" id="chat_entry_box" >
                    <input type='text' placeholder="Your Text Here!" ref={chat} className="chat_input_area" />
                    <button className='edu-submit' type="submit">
                        Send
                    </button>
                </form>
            </div>
        </div>
    );
}

export default ChatWindow;