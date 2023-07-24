/* Display one chat entry.
 */

import React, { useState, useEffect } from 'react';
import "./group_chat_entry.css"

function GroupChatEntry(props) {
    const [_message, setMessage] = useState(props.message)
    const [_fromSelf, setFromSelf] = useState(props.fromSelf)
    const [_user, setUser] = useState(props.user)

    // determine value of message div className
    const messageType = _fromSelf ? 'student_from_other' : 'student_from_self'; 
    const messageTypeClass = _fromSelf ? ' student_from_other_name' : ' student_from_self_name'; 
    const messageTypeDiv = _fromSelf ? 'student_from_other_div' : 'student_from_self_div';               //Current user
        
    return (
      <div className={messageTypeDiv}>
        
        <div className={messageTypeClass}>
          {_user}
        </div>
        
        <div className={messageType}>
          {_message}
        </div>
      </div>
    );
}

export default GroupChatEntry;    
   



