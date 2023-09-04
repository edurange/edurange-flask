import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import Convert from 'ansi-to-html';
import './SSH_web.css'

const SSH_web = (props = {}) => {
    const [output, setOutput] = useState([]);
    const [input, setInput] = useState('');
    const [socket, setSocket] = useState(null);

    // Initialize ansi-to-html converter
    const converter = new Convert({
        fg: '#FFF',
        newline: true,
        bg: "#FFF"
    });

    useEffect(() => {
        const newSocket = io.connect('http://10.0.0.55:31337');
        setSocket(newSocket);

        newSocket.on('edu3_response', (data) => {
            console.log("Received data from server:", data);
            const htmlOutput = converter.toHtml(data.result.replace(/\n/g, "<br>"));
            setOutput(oldOutput => [...oldOutput, htmlOutput]);
        });

        return () => newSocket.close();
    }, []);

    useEffect(() => {
        const outputFrame = document.querySelector('.ssh-terminal-output-content');
        if (outputFrame) {
            outputFrame.scrollTop = outputFrame.scrollHeight;
        }
    }, [output]);

    const handleInputSubmit = () => {
        if (socket) {
            socket.emit('edu3_command', { command: input });
            setInput('');  // clear the input after sending
        } else {
            console.error('Socket is not connected.');
        }
    }

    return (
        <div className="ssh-terminal-frame">
            <div className='ssh-terminal-header-frame'>
                <div className='ssh-terminal-header-text'>
                    Welcome to the eduRange pseudo-terminal
                </div>
            </div>
            
            <div className='ssh-terminal-output-frame'>
                <div className='ssh-terminal-output-content'>
                    <div className="ssh-terminal-output-item" dangerouslySetInnerHTML={{ __html: output.join('') }}></div>
                </div>
            </div>
            
            <div className='ssh-terminal-input-frame'>
                <input 
                    type="text"
                    value={input}
                    className='ssh-terminal-input-text'
                    onChange={e => setInput(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && handleInputSubmit()}
                />

            </div>
        </div>
    );
};

export default SSH_web;
