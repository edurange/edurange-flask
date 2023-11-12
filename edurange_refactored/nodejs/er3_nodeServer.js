const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const er3_ssh = require('./er3_modules/er3_ssh');

const SERVER_PORT = 31337;

const er3_nodeApp = express();
const er3_nodeServer = http.createServer(er3_nodeApp);
const er3_socketIO = socketIo(er3_nodeServer, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

er3_nodeApp.use(cors());

er3_ssh(er3_socketIO);  // init ssh 'app' w/ socket.io

er3_nodeServer.listen(SERVER_PORT, () => {
    console.log(`er3_nodeServer listening on port ${SERVER_PORT}`);
});
