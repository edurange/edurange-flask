var _path = require('path'); 
const dotEnvPath = _path.resolve(process.cwd(), '.env');
const dotenv = require('dotenv').config({ path: dotEnvPath }); //grabbing the port number from the .env file

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
        origin: [ "https://" + process.env.HOST_EXTERN_ADDRESS  + ":5000",
                  "http://" + process.env.HOST_EXTERN_ADDRESS  + ":5000",
                  "https://" + process.env.HOST_EXTERN_ADDRESS  + ":443",
                  "http://" + process.env.HOST_EXTERN_ADDRESS  + ":80",
                ],

        // accept these types of HTTP requests
        methods: ["GET", "POST"],
    },
});

// first irun npm install pg
const pg = require('pg')

// Pool objects use environment variables
// for connection information

// TO DO: Change .env file to vibe with this better
// make it default: use PGHOST, PGUSER, PGPASSWORD, PGDATABASE, and PGPORT
const pool = new pg.Pool({
  connectionString: process.env.DATABASE_URL
});


//create middleware
io.use((socket, next) => {
  const uid = socket.handshake.auth.uid;
  if(!uid) {
    return next(new Error("no user ID"));
  }
  socket.uid = uid;
  console.log("UID!")

  const sid = socket.handshake.auth.sid;
  if(!sid) {
    return next(new Error("no scenario ID"));
  }
  socket.sid = sid;

  console.log("SID!")
  
  
  next();
});


io.on('connection', socket => {

  for(let i in studentList) {
    
    let x_uid = (parseInt(i) + 1).toString()
    
    // 
    if(!masterListChats[x_uid] || !masterListChats[x_uid].messages)  {
      masterListChats[x_uid] = {
        messages: [],
      }
    }

    if(!masterLiveStuds[x_uid] || !masterLiveStuds[x_uid].live)  {
      masterLiveStuds[x_uid] = {
        live: false,
      }
    }
  }


  if (masterListChats[socket.uid] && masterListChats[socket.uid].messages) {
    if(socket.uid!="000") {
      prevChat = masterListChats[socket.uid].messages;
      console.log(`Prev chat for student#${socket.uid}: ${JSON.stringify(prevChat)}`)
      socket.emit("student session retrieval",prevChat);
      socket.emit("group session retrieval", prevChat);
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
  
  //var msg_list = [];
  // send room members message so they can make server-side update
  socket.on("send message", ({messageContents, _to, _from}) => {
/*
    const chatDB_rowEntry = [_from,_to,messageContents, alertTime, socket.sid]
    const query = 'INSERT INTO chat_history (sender, recipient, message_contents, timestamp, sid) VALUES ($1, $2 ,$3, $4, $5)';
    pool.query(query, chatDB_rowEntry, (err, result) => {
      if (err) {
        console.error('Error executing query', err);
      } else {
        console.log('Query result:', result.rows);
      }
    });
    */
    var room = (_to!=="000") ? _to : _from; // room number is student's unique id#
    
    masterListChats[room].messages.push({               
      contents: messageContents,
      from: _from,
        to: _to,
    });

    msg_list = masterListChats[socket.uid].messages;


    // student messages alert instructor
    if(_from!=="000") {
      msg_list = masterListChats[socket.uid].messages;
      trafficAlert("message", {msg_list, room});
    }
    io.to(room).emit("new message", {messageContents, _to, _from, room}); // all room members sent message
  });
  
  socket.on("send group message", ({messageContents, _from}) => {

    const chatDB_rowEntry = [_from ,messageContents, alertTime, socket.sid]
    const query = 'INSERT INTO group_chat_history (sender, message_contents, timestamp, sid) VALUES ($1, $2 ,$3, $4)';
    pool.query(query, chatDB_rowEntry, (err, result) => {
      if (err) {
        console.error('Error executing query', err);
      }
    });

    async function getUsername() {
      try {
        const uname_query = 'SELECT username FROM users WHERE id=$1';
        const result = await pool.query(uname_query, [_from]);

        if (result.rows.length > 0) {
          const users_name = result.rows[0].username;
          console.log(`Username: ${users_name}`);
          return users_name;
        } else {
          console.log('User not found.');
        }
      } catch (err) {
        console.error('Error executing query:', err);
      }
      return;
    }


    msg_list = masterListChats[socket.uid].messages;
    
    // student messages alert instructor
    if(_from!=="000") {
      room = socket.uid
      trafficAlert("message", {msg_list, room});
    }

    //io.emit("new group message", {messageContents, _from}); // all group members sent message

    async function queryThenEmit() {
      try {
        const _uname = await getUsername()
        if(_uname) {

          masterListChats[socket.uid].messages.push({               
            contents: messageContents,
            from: _from,
            uname: _uname,
          });
          io.emit("new group message", {messageContents, _from, _uname})
        } else {
          console.log("No uname found.")
        }
      } catch (err) {
        console.error('Error executing query:', err);
      }
    }

    queryThenEmit()

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

console.log(`sever listening on port ${process.env.CHAT_SERVER_PORT}`);
io.listen(process.env.CHAT_SERVER_PORT);