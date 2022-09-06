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
        origin: "http://localhost:5000",

        // accept these types of HTTP requests
        methods: ["GET", "POST"],
    },
});

io.on('connection', socket => {
  console.log(`connect: ${socket.id}`);

  socket.on('hello!', () => {
    console.log(`hello from ${socket.id}`);
  });

  socket.on('disconnect', () => {
    console.log(`disconnect: ${socket.id}`);
  });
});

io.listen(3001);

setInterval(() => {
  io.emit('message', new Date().toISOString());
}, 1000);
