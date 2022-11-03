/* Display one chat session.
 */

import "./student_chat_window.css"
import React, { useState, useEffect } from 'react';
import StudentChatEntry from "../student_chat_entry/student_chat_entry.component";
//import ChatInput from "../chat_input/chat_input.component";



function StudentChatWindow({messages, chat_opened}) {
    const [user, setUser] = useState("");  
    const [input, setInput] = useState("");                      //Current user
    const [displayMessages, setDisplayMessages] = useState(null);
    const chat = React.createRef();   
    
    useEffect(()=>{
        setDisplayMessages(messages)
     }, [messages]);                       //Input entry for chat

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

    function getMessagesContent() {  
        if(displayMessages) { 
            let messageList = displayMessages.map((message) =>             //Map the messages to a component
                <StudentChatEntry key={Math.random() * 100} 
                message={message.contents} 
                fromSelf={message.from=="000"} 
                user={message.from!="000"?"me":"The Benevolent Instructor"} 
                />
            )
            return messageList;                                     //Return the componenet for rendering
        }
        return;
    }

    function onSubmit(e) {                                        //Send input as a chat message
        e.preventDefault();
        setInput("");//Clear current message from input      
    }

    const onChange = (e) => {
        setInput(e.target.value);
        console.log("INPUT" + input);
    }
    
    return(
         <div id='studentChatWindow'>
          {getMessagesContent(displayMessages)}
           {/*} <div id='student_chat_input'>
                <form onSubmit={onSubmit} autoComplete="off" id="student_chat_entry_box" >
                    <input 
                        type='text'
                        placeholder="Your Text Here!"
                        onChange={onChange}
                        value= {input} 
                        ref={chat}
                        className="chat_input_area" 
                        />
                    <button className='student_chat_submit' type="submit">
                        Send
                    </button>
                </form>
            </div>
            */}
        </div>
    );
}

export default StudentChatWindow;