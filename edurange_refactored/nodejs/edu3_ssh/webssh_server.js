const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const { Client } = require('ssh2');
// const webssh2App = require('./webssh2/app');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

const SERVER_PORT = 31337;

// Middleware for CORS
app.use(cors());

// webssh2 route
// app.use('/webssh', webssh2App);

io.on('connection', (socket) => {
    console.log('New client connected');

    // Send greeting to the newly connected client
    socket.emit('greeting', { 
        greeting: `\x1b[37m Welcome to the \x1b[32medu\x1b[31mRange\x1b[30m pseudo-terminal! \n \x1b[37mWhile we recommend using official OS terminal shells and ssh connections, this \x1b[35m(limited feature)\x1b[37m emulated terminal can also be handy.\x1b[0m \n\n`
    });

    socket.on('set_credentials', (reqBody) => {
        const sshClient = new Client();

        sshClient.on('ready', () => {
            console.log('SSH Client Ready');

            sshClient.shell((err, shell) => {
                if (err) {
                    console.error("Error starting shell:", err);
                    return;
                }

                let bufferedData = "";
                shell.on('data', (dataOutput) => {
                    bufferedData += dataOutput.toString();

                    if (dataOutput.toString().trim().endsWith("$")) {
                        const output = `${bufferedData}`;

                        socket.emit('edu3_response', { result: output });
                        bufferedData = "";
                    }
                });

                socket.on('edu3_command', (data) => {
                    shell.write(data.command + "\n");
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

server.listen(SERVER_PORT, () => {
    console.log(`webSSH server listening on port ${SERVER_PORT}`);
});
