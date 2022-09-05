/*1. import express */
/*2. app variable set to instance of express function */
/*3. http variable grabbed from http library (inherent to npm) */
/*4. import cors library */
/*5. import a CLASS from socket.io library */

/*1.*/const express = require("express");
/*2.*/const app = express();
/*3.*/const http = require("http");
/*4.*/const cors = require("cors");
/*5.*/const { Server } = require("socket.io");

//
app.use(cors());


// create server
const server = http.createServer(app);

// create new instance of { Server } class
const io = new Server(server, {
    // CORS = cross-origin resource sharing
    // allows server-client communication 
    cors: {
        // accept communication with this port
        origin: "http://localhost:3000",

        // accept these types of HTTP requests
        methods: ["GET", "POST"],
    },
});

// when user connects...
io.on("connection", (socket) => {
    console.log(`User connected ${socket.id}`);

    /*
    // "join_room" is a function called in App.js
    socket.on("join_room", (data) => {
        socket.join(data);
        console.log(`User with ID ${socket.id} joined room ${data}`);
    });
    */
    socket.emit("connect");

    // "sendd_message" is a function called in Chat.js
    socket.on("message", (/*data*/) => {
        // room is in the array of data var passed
        //socket.to(data.room).emit("receive_message", data);

        socket.emit("receive_message");
    });

    // when user disconnects...
    socket.on("disconnect", () => {
        console.log("User disconnected", socket.id)
    });
});

// server listens from port 3001
server.listen(3001, () => {
    console.log("SERVER RUNNING");
  });

