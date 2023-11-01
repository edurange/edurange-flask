import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import Convert from 'ansi-to-html';
import './SSH_web.css'

const NODEJS_WEBSSH_IP = "10.0.0.55:31337"

const brightOnDark = {
    0: '#839496',  // Black
    1: '#fc0303',  // Red
    2: '#84fc03',  // Green
    3: '#fff654',  // Yellow
    4: '#2db3ff',  // Blue
    5: '#ff0096',  // Magenta
    6: '#00d9c7',  // Cyan
    7: '#ffffff',  // White
};

function SSH_web (props) {
    const [output, setOutput] = useState([]);
    const [input, setInput] = useState('');
    const [socket, setSocket] = useState(null);

    const [SSH_ip, SSH_port_str] = props.SSH_address.split(':');
    const SSH_port = parseInt(SSH_port_str, 10);
    const SSH_username = props.SSH_username;
    const SSH_password = props.SSH_password;

    // Initialize ansi-to-html converter
    const converter = new Convert({
        colors: brightOnDark,
        newline: true,
    });

    useEffect(() => {
        const newSocket = io.connect(`http://${NODEJS_WEBSSH_IP}`);
        
        // Wait until the socket has connected, then send credentials
        newSocket.on('connect', () => {
            newSocket.emit('set_credentials', { 
                SSH_username: SSH_username, 
                SSH_password: SSH_password,
                SSH_ip: SSH_ip,
                SSH_port: SSH_port
            });
        });
    
        // Listen for the ANSI greeting
        newSocket.on('greeting', (data) => {
            const htmlGreeting = converter.toHtml(data.greeting);
            // const htmlGreeting = converter.toHtml(data.greeting.replace(/\n/g, "<br>"));
            setOutput(oldOutput => [htmlGreeting, ...oldOutput]);
        });
        
        newSocket.on('edu3_response', (data) => {
            // console.log("Received data from server:", data);
            // const htmlOutput = converter.toHtml(data.result.replace(/\n/g, "<br>"));
            const htmlOutput = converter.toHtml(data.result);
            setOutput(oldOutput => [...oldOutput, htmlOutput]);
        });
        
        setSocket(newSocket);
        return () => newSocket.close();
    }, []);
    
    

    useEffect(() => {
        const outputFrame = document.querySelector('.ssh-terminal-output-content');
        if (outputFrame) {
            outputFrame.scrollTop = outputFrame.scrollHeight;
        }
    }, [output]);

    function handleInputSubmit () {
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
                    eduRange pseudo-terminal
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
