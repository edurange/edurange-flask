/* Display one chat session.
 */

import "./student_chat_window.css"
import React, { useState, useEffect } from 'react';
import StudentChatEntry from "../student_chat_entry/student_chat_entry.component";
//import ChatInput from "../chat_input/chat_input.component";



function StudentChatWindow({messages, chat_opened}) {                    //Current user
    const [displayMessages, setDisplayMessages] = useState(null);
    //const chat = React.createRef();   
    
    useEffect(()=>{
        console.log("Student Chat Windows :: messages now:: : " + JSON.stringify(messages));
        if(messages) {
            setDisplayMessages(messages)
        }
     }, [messages]);                       //Input entry for chat

    function getMessagesContent() {
        if(displayMessages) { 
            let messageList = displayMessages.map((message) =>  
                //Map the messages to a component
                <StudentChatEntry key={Math.random() * 100} 
                    message={message.contents} 
                    fromSelf={message.from=="000"} 
                    user={message.from!="000"?"me":"Instructor"}
                />
            )
            return messageList;                                     //Return the componenet for rendering
        }
        return;
    }
    
    return(
         <div id='studentChatWindow'>
          {getMessagesContent(displayMessages)}
        </div>
    );
}

export default StudentChatWindow;
