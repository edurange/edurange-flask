var _path = require('path'); 
const dotEnvPath = _path.resolve(process.cwd(), '.env');

//grabbing the port number from the .env file
const dotenv = require('dotenv').config({ path: dotEnvPath });

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

// REPLACE THIS WITH EXISTING ID IN DATABASE
const crypto = require("crypto");
const randomId = () => crypto.randomBytes(8).toString("hex");

// The session store keeps information necessary to regain
// room access upon reconnection.
const { InMemorySessionStore } = require("./sessionStore");
const sessionStore = new InMemorySessionStore();

// The message store keeps an array of messages, including
// data about message sender and recipient.
const { InMemoryMessageStore } = require("./messageStore");
const messageStore = new InMemoryMessageStore();

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
        // HTTP vs HTTPS BIG ISSUE FIXED FOR NOW BY dArKsEtH THANKS
        origin: [ "https://" + process.env.HOST_EXTERN_ADDRESS  + ":5000",
                  "http://" + process.env.HOST_EXTERN_ADDRESS  + ":80",
                  "https://" + process.env.HOST_EXTERN_ADDRESS  + ":443",
                  "http://" + process.env.HOST_EXTERN_ADDRESS  + ":5000"
                ],

        // accept these types of HTTP requests
        methods: ["GET", "POST"],
    },
});

// Registering middleware:
    // - uses sessionID to retrieve session
io.use((socket, next) => {
    const sessionID = socket.handshake.auth.sessionID;
    if (sessionID) {
      const session = sessionStore.findSession(sessionID);
      if (session) {
        socket.sessionID = sessionID;
        socket.userID = session.userID;
        socket.username = session.username;
        return next();
      }
    }
    const username = socket.handshake.auth.username;
    if (!username) {
      return next(new Error("invalid username"));
    }
    socket.sessionID = randomId();
    socket.userID = randomId();
    socket.username = username;
    next();
});

io.on("connection", (socket) => {
    // persist session
    sessionStore.saveSession(socket.sessionID, {
      userID: socket.userID,
      username: socket.username,
      connected: true,
    });
    
    // emit session details
    socket.emit("session", {
    sessionID: socket.sessionID,
    userID: socket.userID,
    });
    
    // join the "userID" room
    socket.join(socket.userID);
    

    // EDIT: this only needs to happen for INSTRUCTOR
    // fetch existing users
    const users = [];
    const messagesPerUser = new Map();
    messageStore.findMessagesForUser(socket.userID).forEach((message) => {
      const { from, to } = message;
      const otherUser = socket.userID === from ? to : from;
      if (messagesPerUser.has(otherUser)) {
        messagesPerUser.get(otherUser).push(message);
      } else {
        messagesPerUser.set(otherUser, [message]);
      }
    });
    sessionStore.findAllSessions().forEach((session) => {
      users.push({
        userID: session.userID,
        username: session.username,
        connected: session.connected,
        messages: messagesPerUser.get(session.userID) || [],
      });
    });
    socket.emit("users", users);
    
    // notify existing users
    socket.broadcast.emit("user connected", {
      userID: socket.userID,
      username: socket.username,
      connected: true,
      messages: [],
    });
    console.log(`Generared userID: ${socket.username}`);

    // forward the private message to the right recipient (and to other tabs of the sender)
    socket.on("private message", ({ content, to }) => {
      const message = {
      content,
      from: socket.userID,
      to,
    };
    // forwarding to self (other tabs open) and intended recipient. 
    socket.to(to).to(socket.userID).emit("private message", message);
      messageStore.saveMessage(message);
    });
    
    // notify users upon disconnection
    socket.on("disconnect", async () => {
      const matchingSockets = await io.in(socket.userID).allSockets();
      const isDisconnected = matchingSockets.size === 0;
      if (isDisconnected) {
    // notify other users
        socket.broadcast.emit("user disconnected", socket.userID);
        // update the connection status of the session
        sessionStore.saveSession(socket.sessionID, {
          userID: socket.userID,
          username: socket.username,
          connected: false,
        });
        }
      });
    });


const PORT = process.env.CHAT_SERVER_PORT || 3000;

httpServer.listen(PORT, () =>
  console.log(`server listening at http://localhost:${PORT}`)
);

