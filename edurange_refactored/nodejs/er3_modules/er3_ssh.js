// working ssh terminal server config (uses xterm)

const { Client } = require('ssh2');
module.exports = function (io) {

    io.on('connection', (socket) => {
        console.log('New client connected');
    
        // Send greeting to the newly connected client
        socket.emit('greeting', { 
            greeting: `\x1b[37m Welcome to the \x1b[32medu\x1b[31mRange\x1b[30m pseudo123-terminal! \n \x1b[37mWhile we recommend using official OS terminal shells and ssh connections, this \x1b[35m(limited feature)\x1b[37m emulated terminal can also be handy.\x1b[0m \n\n`
        });
    
        socket.on('set_credentials', (reqBody) => {
            const sshClient = new Client();
            let sendTimer = null;
            const SEND_INTERVAL = 10;  // send data every 10ms
            let bufferedData = ""; // Moved to this scope
    
            function sendDataToFrontend() {
                if (bufferedData) {
                    socket.emit('edu3_response', { result: bufferedData });
                    bufferedData = "";
                };
            };
    
            sshClient.on('ready', () => {
                console.log('SSH Client Ready');
    
                sshClient.shell((err, shell) => {
                    if (err) {
                        console.error("Error starting shell:", err);
                        return;
                    };
    
                    shell.on('data', (dataOutput) => {
                        bufferedData += dataOutput.toString();
    
                        if (sendTimer) clearTimeout(sendTimer);
    
                        if (dataOutput.toString().trim().endsWith("$")) {
                            sendDataToFrontend();
                        } else {
                            sendTimer = setTimeout(sendDataToFrontend, SEND_INTERVAL);
                        }
                    });
    
                    socket.on('edu3_command_data', (data) => {
                        shell.write(data.data);
                    });
                    
    
                    shell.on('close', () => {
                        console.log('Shell session closed');
                    });
    
                    shell.stderr.on('data', (dataError) => {
                        console.log('Error from shell:', dataError.toString());
                    });
    
                });
    
            }).connect({
                host: reqBody.SSH_ip,
                port: reqBody.SSH_port,
                username: reqBody.SSH_username,
                password: reqBody.SSH_password,
            });
    
            socket.on('disconnect', () => {
                console.log('Client disconnected');
                sshClient.end();
            });
        });
    });
    return io;
}