import React, { useState, useRef, useEffect } from 'react';
import './SSHmodal.css';

const initialData = [
    { 
        ip: "127.0.0.1",
        port: "5000",
        password: "superSecurePass",
        username: "exampleUser"  // Step 1: Added initial username
    }
];

const SSHmodal = () => {
    const [currentData, setCurrentData] = useState(initialData);
    const [isVisible, setIsVisible] = useState(true);
    const innerFrameRef = useRef(null);

    useEffect(() => {
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const handleClickOutside = (event) => {
        if (innerFrameRef.current && !innerFrameRef.current.contains(event.target)) {
            setIsVisible(false);
        }
    };

    const generateRandomData = () => {
        const randomIP = `${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}`;
        const randomPort = `${Math.floor(Math.random() * 10000)}`;
        const randomPassword = Math.random().toString(36).substring(2, 10);
        const randomUsername = `user${Math.random().toString(36).substring(2, 6)}`;
        setCurrentData([
            { ip: randomIP, port: randomPort, password: randomPassword, username: randomUsername }
        ]);
    };

    const copyToClipboard = () => {
        const sshCommand = `ssh ${currentData[0].username}@${currentData[0].ip} -p ${currentData[0].port}`;
        navigator.clipboard.writeText(sshCommand).then(() => {
            console.log('SSH Command copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy!', err);
        });
    };

    if (!isVisible) return null;

    return (
        <div className="SSHmodal-outerFrame">
            <div className="SSHmodal-innerFrame" ref={innerFrameRef}>
                {currentData.map((item, index) => (
                    <React.Fragment key={index}>
                        <div className="SSHmodal-row">
                            <span>IP</span>
                            <span>{item.ip}</span>
                        </div>
                        <div className="SSHmodal-row">
                            <span>Port</span>
                            <span>{item.port}</span>
                        </div>
                        <div className="SSHmodal-row">
                            <span>Username</span>
                            <span>{item.username}</span>
                        </div>
                        <div className="SSHmodal-row">
                            <span>Password</span>
                            <span>{item.password}</span>
                        </div>
                    </React.Fragment>
                ))}
                <div className="SSHmodal-buttonSection">
                    <div className="SSHmodal-button" onClick={generateRandomData}>
                        Generate
                    </div>
                    <div className="SSHmodal-button" onClick={copyToClipboard}>
                        Clipboard
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SSHmodal;
