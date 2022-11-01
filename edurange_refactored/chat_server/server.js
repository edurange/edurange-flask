

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

//create middleware
io.use((socket, next) => {
  const uid = socket.handshake.auth.uid;
  if(!uid) {
    return next(new Error("no user ID"));
  }
  socket.uid = uid;
  next();
});


io.on('connection', socket => {
  const emit_users = (alertType) => {
    let alertString = {};
    alertTime = new Date().toISOString()
    .replace('T', ' ')
    .replace('Z', '');
    if (socket.uid!=="000") {
      alertString = {
        uid: socket.uid,
        username: studentList[socket.uid-2],
        id: studentList[socket.uid-2],
        type:  alertType,
        time: alertTime,
        };
      }
    console.log(JSON.stringify(alertString));
    socket.to("000").emit("alert", alertString);
    console.log(io.sockets.adapter.rooms); // servers rooms maps.
  }

  socket.on("connect_error", err => {
    console.log("Connnection Error: no user id.")
  });

  //join rooms. 
  socket.join(socket.uid); //students join their own room. 
  if(socket.uid=="000") { //instructors join everyone else's.
    socket.join("000");
    for(let key in studentList) {
      socket.join(key);
    }
  }

  const messages = [];
  socket.on("new message", ({messageContents, _to, _from}) => {
    let recipient = (_to=="instructor") ? "000" : _to; 
    messages.push({
      contents: messageContents,
      from: _from,
      to: recipient,
    });
    socket.to(recipient).emit("new message")
  });

  //emit join alert.
  emit_users("studJoin");

  socket.on("disconnect", () => {
    emit_users("studLeave");
  });

});

console.log(`sever listening on port ${process.env.CHAT_SERVER_PORT}`)
io.listen(process.env.CHAT_SERVER_PORT);
