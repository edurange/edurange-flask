import React, { useEffect, useRef, useState } from 'react';
import io from 'socket.io-client';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';
import './SSH_web.css';

const NODEJS_WEBSSH_IP = "10.0.0.55:31337";

function SSH_web(props) {
    const terminalRef = useRef(null);
    const term = useRef(new Terminal());
    const fitAddon = useRef(new FitAddon());
    const socketRef = useRef(null); 

    const [SSH_ip, SSH_port_str] = props.SSH_address.split(':');
    const SSH_port = parseInt(SSH_port_str, 10);
    const SSH_username = props.SSH_username;
    const SSH_password = props.SSH_password;

    useEffect(() => {
        term.current.loadAddon(fitAddon.current);
        term.current.open(terminalRef.current);
        fitAddon.current.fit();

        const newSocket = io.connect(`http://${NODEJS_WEBSSH_IP}`);
        socketRef.current = newSocket;  // Store the socket in the ref.

        newSocket.on('connect', () => {
            newSocket.emit('set_credentials', { 
                SSH_username: SSH_username, 
                SSH_password: SSH_password,
                SSH_ip: SSH_ip,
                SSH_port: SSH_port
            });
        });
    
        newSocket.on('greeting', (data) => {
            term.current.write(data.greeting);
        });
        
        newSocket.on('edu3_response', (data) => {
            term.current.write(data.result);
        });


        term.current.onData(data => {
            if (socketRef.current) {
                socketRef.current.emit('edu3_command_data', { data: data });
            } else {
                console.error('Socket is not connected.');
            }
        });

        return () => {
            newSocket.close();
            term.current.dispose();
        };
    }, []);

    return (
        <div className="ssh-terminal-frame">
            <div className='ssh-terminal-header-frame'>
                <div className='ssh-terminal-header-text'>
                    eduRange pseudo-terminal
                </div>
            </div>
            
            <div className='ssh-terminal-output-frame' ref={terminalRef}></div>
        </div>
    );
};

export default SSH_web;
