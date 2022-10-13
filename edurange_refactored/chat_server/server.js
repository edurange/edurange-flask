

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

const crypto = require("crypto");
const randomId = () => crypto.randomBytes(8).toString("hex");

const { InMemorySessionStore } = require("./sessionStore");
const sessionStore =  new InMemorySessionStore();

const { InMemoryMessageStore } = require("./messageStore");
const messageStore = new InMemoryMessageStore();

io.use((socket, next) => {
  const sessionID = socket.handshake.auth.sessionID;
  if (sessionID) {
    const session = sessionStore.findSession(sessionID);
    if (session) {
      socket.sessionID = sessionID;
      socket.userID = session.userID;
      socket.isInstructor = session.isInstructor;
      return next();
    }
  }
  socket.sessionID = randomId();
  socket.userID = randomId();
  socket.isInstructor = false;
  next();
});



io.on('connection', socket => {


  //initally save sessions
  // persist session
 sessionStore.saveSession(socket.sessionID, {
  userID: socket.userID,
  connected: true,
  });

  // emit session details
  socket.emit("session", {
  sessionID: socket.sessionID,
  userID: socket.userID,
  isInstructor: socket.isInstructor,
  });



  //recieve the correct ID
  socket.on("studentID", (studentID) => {
    socket.userID = studentID;
    sessionStore.saveSession(socket.sessionID, {
      userID: studentID,
      });    
  });

  // join arbitrary room
  const roomName = socket.id;
  socket.join(roomName);
  //io.emit("room_joined", roomName);

  console.log(`connect: ${socket.id}`);

  socket.on('hello!', () => {
    console.log(`hello from ${socket.id}`);
  });

  socket.on('disconnect', () => {
    console.log(`disconnect: ${socket.id}`);
  });


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
     connected: session.connected,
     messages: messagesPerUser.get(session.userID) || [],
   });
 });
 socket.emit("users", users);

 // notify existing users
 socket.broadcast.emit("user connected", {
   userID: socket.userID,
   connected: true,
   messages: [],
 });
 // forward the private message to the right recipient (and to other tabs of the sender)
 socket.on("message", ({ content, to }) => {
   const message = {
     content,
     from: socket.userID,
     to,
   };
   socket.to(to).to(socket.userID).emit("message", message);
   messageStore.saveMessage(message);
 });



});

console.log(process.env.CHAT_SERVER_PORT);
io.listen(process.env.CHAT_SERVER_PORT);
