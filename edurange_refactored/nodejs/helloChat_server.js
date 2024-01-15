
const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

// Initialize Express app and HTTP server
const app = express();
const webServer = http.createServer(app);

// Initialize Socket.IO and enable CORS
const io = socketIO(webServer, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

// Serve static files from 'public' directory (where your HTML file will be)
app.use(express.static(path.join(__dirname, 'public')));

// Chat log file path
const logFilePath = path.join(__dirname, 'chat_log.csv');

// Function to log chat messages to CSV
const logChatToCSV = (message) => {
    const logEntry = `${new Date().toISOString()}, "${message}"\n`;
    fs.appendFileSync(logFilePath, logEntry);
};

// Handle Socket.IO connections
io.on('connection', (socket) => {
    console.log('A user connected');

    socket.on('chat message', (msg) => {
        console.log('Received message:', msg);
        // Log message to CSV
        logChatToCSV(msg);
        // Broadcast message to all clients
        io.emit('chat message', msg);
    });

    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});

// Set the webServer to listen on a port
const PORT = 37731;
webServer.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
