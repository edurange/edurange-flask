

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
// used for sockets joining room
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
        // DarkSeth temp fix.
        origin: [ "https://" + process.env.HOST_EXTERN_ADDRESS  + ":5000",
                  "http://" + process.env.HOST_EXTERN_ADDRESS  + ":5000",
                  "https://" + process.env.HOST_EXTERN_ADDRESS  + ":443",
                  "http://" + process.env.HOST_EXTERN_ADDRESS  + ":80",
                ],

        // accept these types of HTTP requests
        methods: ["GET", "POST"],
    },
});

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
  
  // Error handler for middleware.
  socket.on("connect_error", err => {
    console.log("Connnection Error: no user id.")
  });

  // Sockets join rooms immediately after connecting. 
  socket.join(socket.uid); //students join their own room. 
 
  if(socket.uid=="000") { //instructors join everyone else's.
    socket.join("000");
    for(let key in studentList) {
      socket.join(key);
    }
  }
  // Error Logging -- console.log(io.sockets.adapter.rooms); // servers rooms maps.

    // Traffic Alerts: Join, Leave, Message.
  const trafficAlert = (alertType) => {
    let alertString = {};
    // timestamp for event
    alertTime = new Date().toISOString() 
    .replace('T', ' ')
    .replace('Z', '');

    // Sockets belonging to students create alerts for instructor
    if (socket.uid!=="000") {
      alertString = {
        uid: socket.uid,
        username: studentList[socket.uid-2], // (the first user's database ID is "2")
        id: studentList[socket.uid-2],
        type:  alertType,
        time: alertTime,
        };
    }
    socket.to("000").emit("alert", alertString);  //emit alert.
  }

  var msg_list = [];
  // send room members message so they can make server-side update
  socket.on("send message", ({messageContents, _to, _from}) => {
    var room = (_to!=="000") ? _to : _from; // room number is student's unique id#
    io.to(room).emit("new message", {messageContents, _to, _from, room}); // all room members sent message
  });

  // push recieved message to msg_list array
  // send entire list
  socket.on("request msg_list", ({messageContents, _to, _from, room}) => {
    // both members keep track of message discourse in case of disconnection
    msg_list.push({               
      contents: messageContents,
      from: _from,
        to: _to,
    });
    
    // student messages alert instructor
    if(_from!=="000") {
      trafficAlert("message");
    }

    // students capture specific student instructor correspondance
    if(socket.uid===room) {
      io.to(room).emit("msg_list update", {msg_list, room});
    }
  });

  //emit join alert.
  trafficAlert("studJoin");

  socket.on("disconnect", () => {
    trafficAlert("studLeave");
  });

});

console.log(`sever listening on port ${process.env.CHAT_SERVER_PORT}`)
io.listen(process.env.CHAT_SERVER_PORT);
