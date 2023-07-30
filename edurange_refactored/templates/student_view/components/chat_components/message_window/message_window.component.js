import React, { useState, useEffect } from 'react';

import "../message/message.component"
import StudentChatEntry from '../../student_chat_entry/student_chat_entry.component';

function MessageWindow(props) {

    function renderMessages() {
        if(props.messages) {
            let messageList = props.messages.map((message_entry) => {
                <StudentChatEntry
                    key = {Math.random() * 100}
                    message={message_entry.message}
                    from_self={message.recipient==props.uid}
                />
            });
            return messageList;
        }
        return;
    }
    
    return (
        <div>
            {renderMessages()}
        </div>
    );
}

export default MessageWindow;