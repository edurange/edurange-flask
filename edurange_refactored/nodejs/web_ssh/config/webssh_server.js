const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const { Client } = require('ssh2');

const webssh_app = express();
const webssh_server = http.createServer(webssh_app);
const webssh_io = socketIo(webssh_server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});
const PORT = 31337;

webssh_app.use(cors());
webssh_app.use(express.static('public'));

webssh_io.on('connection', (socket) => {
    console.log('New client connected');

    const sshClient = new Client();

    sshClient.on('ready', () => {
        console.log('SSH Client Ready');

        sshClient.shell((err, shell) => {
            if (err) {
                console.error("Error starting shell:", err);
                return;
            }

            console.log('Shell session started'); // Log the start of the shell session

            let bufferedData = "";

            shell.on('data', (dataOutput) => {
                console.log('Data chunk received from shell:', dataOutput.toString()); 
                
                bufferedData += dataOutput.toString();

                // Check for command prompt or another way to determine command completion. Adjust based on your system's output.
                if (dataOutput.toString().trim().endsWith("$")) {  
                    // Replace newline characters with the literal string "\n"
                    // bufferedData = bufferedData.replace(/\n/g, "\\n");

                    const output = `Output: ${bufferedData}`;
                    socket.emit('edu3_response', { result: output });
                    bufferedData = "";  // Clear the buffer for the next command
                }
            });

            shell.on('close', () => {
                console.log('Shell session closed');
            });

            shell.stderr.on('data', (dataError) => {
                console.log('Error from shell:', dataError.toString()); // Log any errors from the shell
            });

            socket.on('edu3_command', (data) => {
                console.log(`Received command: ${data.command}`);
                shell.write(data.command + "\n");
            });

        });

    }).connect({
        host: '10.0.0.55',
        port: 32774,
        username: 'ttttuser1',
        password: '9RZ3d9v7slIpJVTk',
    });

    socket.on('disconnect', () => {
        console.log('Client disconnected');
        sshClient.end();
    });
});

webssh_server.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
