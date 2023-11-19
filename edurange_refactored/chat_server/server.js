var _path = require('path'); 
const dotEnvPath = _path.resolve(process.cwd(), '.env');
const dotenv = require('dotenv').config({ path: dotEnvPath }); //grabbing the port number from the .env file

const express = require("express");
const app = express();
const http = require("http");
const cors = require("cors");
const { Server } = require("socket.io");
//const chat_post = require("contents.py");

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

//dictionary of chat sessions
let masterListChats = {};
let masterLiveStuds = {};

// create new instance of { Server } class
const io = new Server(server, {
    // CORS = cross-origin resource sharing
    // allows server-client communication 
    cors: {
        // accept communication with this port
        // DarkSeth temp fix.
        origin: [ "*", 
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
  var stream = fs.createWriteStream("logs/chat_server_logs.csv", {flags:'a'});


  for(let i in studentList) {
    let x_uid = (parseInt(i) + 1).toString()
    if(!masterListChats[x_uid] || !masterListChats[x_uid].messages)  {
      masterListChats[x_uid] = {
        messages: [],
      }
      let json = JSON.stringify(masterListChats[x_uid]);
    }

    if(!masterLiveStuds[x_uid] || !masterLiveStuds[x_uid].live)  {
      masterLiveStuds[x_uid] = {
        live: false,
      }
    } else {
      //console.log("found previous" + masterLiveStuds[x_uid].live)
    }
  }

  for(let i in studentList) {
    let x_uid = (parseInt(i) + 1).toString();
    //console.log(x_uid + " : " + masterLiveStuds[x_uid].live)
  }


  if (masterListChats[socket.uid] && masterListChats[socket.uid].messages) {
    if(socket.uid!="000") {
      prevChat = masterListChats[socket.uid].messages;
      socket.emit("student session retrieval",prevChat);
    } else {
      instructorPrevChat = masterListChats;
      socket.emit("instructor session retrieval", instructorPrevChat);
    }
  } else {
    masterListChats[socket.uid] = {
      messages: [],
    }
  }
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
    socket.emit("live students", masterLiveStuds);
  }

  
  //console.log(io.sockets.adapter.rooms);

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
        username: studentList[socket.uid-1], // (the first user's database ID is "2")
        id: studentList[socket.uid-1],
        type:  alertType,
        time: alertTime,
        };
    }
    socket.to("000").emit("alert", alertString);  //emit alert.
  }

  //emit join alert.
  if(socket.uid != "000") {
    masterLiveStuds[socket.uid] = { live: true }
  }
  trafficAlert("studJoin");

  //var msg_list = [];
  // send room members message so they can make server-side update
  socket.on("send message", ({messageContents, _to, _from}) => {



    var room = (_to!=="000") ? _to : _from; // room number is student's unique id#
    
    masterListChats[room].messages.push({               
      contents: messageContents,
      from: _from,
        to: _to,
    });

    let currTime = new Date().toISOString() // Ask Aubrey about date formatting for logging
    /*fs.appendFile('./chat_server_logs.csv', `${messageContents}, ${_from}, ${_to}, ${currTime}`, (err) => {
      if(err) {
        console.log(err);
      }
    });*/

    
    stream.write(`${messageContents}, ${_from}, ${_to}, ${currTime}\n`);
    //stream.end();

   const intFrom = parseInt(_from);
   const intTo = parseInt(_to);

    

   // #chat_post.createPost(intFrom, intTo, messageContents);

    msg_list = masterListChats[socket.uid].messages;


    // student messages alert instructor
    if(_from!=="000") {
      msg_list = masterListChats[socket.uid].messages;
      trafficAlert("message", {msg_list, room});
    }
    io.to(room).emit("new message", {messageContents, _to, _from, room}); // all room members sent message
  });
  
  socket.on("disconnect", () => {
    trafficAlert("studLeave");
    if(socket.uid=="000") {
      io.emit("instructor disconnected");
    } else {
      masterLiveStuds[socket.uid] = { live: false }
    }
  });

});

console.log(`sever listening on port ${process.env.CHAT_SERVER_PORT}`)
io.listen(process.env.CHAT_SERVER_PORT);
