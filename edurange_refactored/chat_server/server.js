

var _path = require('path'); 
const dotEnvPath = _path.resolve(process.cwd(), '.env');




//grabbing the port number from the .env file
const dotenv = require('dotenv').config({ path: dotEnvPath });

const express = require("express");
const app = express();
const http = require("http");
const cors = require("cors");
const { Server } = require("socket.io");

app.use(cors());


// create server
const server = http.createServer(app);

// gathering student user ID / username list
const fs = require('fs');
let studentList;
fs.readFile(`${process.env.HOME}/edurange-flask/data/tmp/chatnames.json`, (err, data) => {
    if (err) throw err;
    studentList = JSON.parse(data);
});




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

//TO-DO CREATE SESSION
/*
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
      return next();
    }
  }
  socket.sessionID = randomId();
  socket.userID = randomId();
  next();
});

*/



io.on('connection', socket => {
  const emit_users = () => {
    const users = [];
    for (let [id, socket] of io.of("/").sockets) {
      if (socket.uid!=="000") {
        users.push({
          socketid: id,
          uid: socket.uid,
          username: studentList[socket.uid-1],
        });
      }
    }
    socket.to("000").emit("connected students", users);
    console.log(io.sockets.adapter.rooms); // servers rooms maps.
  }

  // emit session details
  socket.emit("session", {
  sessionID: socket.sessionID,
  userID: socket.userID,
  isInstructor: socket.isInstructor,
  });
  */

  console.log(`connect: ${socket.id} userid: ${socket.userID}`);

  socket.on("student connected", (studentID) => {
      console.log(`student connected: socketID ${socket.id} userID: ${socket.userID}`);
      console.log(`         studentID passed = ${studentID}`);
      console.log(`         # of sockets = ${socket.length}`);
      
  });


});

console.log(process.env.CHAT_SERVER_PORT);
io.listen(process.env.CHAT_SERVER_PORT);
