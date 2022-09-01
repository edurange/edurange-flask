
import React from 'react';
import "./chatbox.styles.css"
import ClientSocket from "../client_socket/client_socket.component"
class Chatbox extends React.Component {
    render() {
        return (
            <div className='edu-chatbox'>
                <ClientSocket />
                <p>Chat me up?</p>
                <input className='type_here' type='text' />
            </div>
        );
    }
}

export default Chatbox;