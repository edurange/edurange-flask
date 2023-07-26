/* Display one chat session.
 */

import "./group_chat_window.css";
import React, { useState, useEffect } from 'react';
import GroupChatEntry from "../group_chat_entry/group_chat_entry.component";
// Pool objects use environment variables
// for connection information

// TO DO: Change .env file to vibe with this better
// make it default: use PGHOST, PGUSER, PGPASSWORD, PGDATABASE, and PGPORT



function GroupChatWindow(props) {   

    const [time, setTime] = useState(new Date());
    const [msg, setMsg] = useState(props._messages)

    useEffect(() => {
      const interval = setInterval(() => {
        setTime(new Date());
      }, 1000);
  
      setMsg(props._messages);
      
      return () => clearInterval(interval);
    }, []);

    function getMessagesContent() {
        if(props._messages) { 
            let messageList = props._messages.map((message) =>  
                //Map the messages to a component
                <GroupChatEntry key={Math.random() * 100} 
                    all_messages = {props._messages}
                    message={message.contents} 
                    fromSelf={message.from==props.user_id} 
                    user={message.uname}
                />
            )
            return messageList;                                     //Return the componenet for rendering
        }
        return null;
    }
    
    return(
         <div id='groupChatWindow'>
          {getMessagesContent()}
        </div>
    );
}

export default GroupChatWindow;