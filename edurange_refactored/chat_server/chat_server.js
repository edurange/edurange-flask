// These are used to define our listening port in our dot env file. 
//var postgres = require('postgres')
var _path = require('path'); 
const dotEnvPath = _path.resolve(process.cwd(), '.env');
const dotenv = require('dotenv').config({ path: dotEnvPath }); //grabbing the port number from the .env file


const express = require("express");
const app = express();

// first irun npm install pg
const pg = require('pg')

// Pool objects use environment variables
// for connection information

// TO DO: Change .env file to vibe with this better
// make it default: use PGHOST, PGUSER, PGPASSWORD, PGDATABASE, and PGPORT
const pool = new pg.Pool({
  host: process.env.HOST_EXTERN_ADDRESS,
  user: 'postgres',
  password: process.env.PASSWORD,
  database: 'flaskdb3',
  port: '5432'
});


pool.query('SELECT * FROM SCENARIOS', (err, result) => {
  if (err) {
    console.error('Error executing query', err);
  } else {
    console.log('Query result:', result.rows);
  }
});

const client = new pg.Client()


//const sql = postgres(`${process.env.DATABASE_URL}`, {})

/*
async function insertUser({ name }) {
  const users = await sql`
    insert into ChatHistory
      (scenario_name)
    values
      (${ name })
    returning scenario_name
  `
  // users = Result [{ name: "Murray", age: 68 }]
  return users
} 

insertUser("Chasmine")
*/



const http = require("http");
const cors = require("cors");
const { Server } = require("socket.io");
app.use(cors());

// create server
const server = http.createServer(app);

// create new instance of { Server } class
const io = new Server(server, {
    // CORS = cross-origin resource sharing.Allows server-client communication.
    cors: {
        // accept communication with this port --- DarkSeth temp fix.
        origin: [ "https://" + process.env.HOST_EXTERN_ADDRESS  + ":5000",
                  "http://" + process.env.HOST_EXTERN_ADDRESS  + ":5000",
                  "https://" + process.env.HOST_EXTERN_ADDRESS  + ":443",
                  "http://" + process.env.HOST_EXTERN_ADDRESS  + ":80",
                ],
        // accept these types of HTTP requests
        methods: ["GET", "POST"],
    },
});

// gathering student user ID / username list, used for sockets joining room
const fs = require('fs'); // fs -- file system module.
let studentList;
fs.readFile(`/home/miranda/edurange-flask/data/tmp/chatnames.json`, (err, data) => {
    if (err) throw err;
    studentList = JSON.parse(data);
});

//dictionary of chat sessions
let masterListChats = {};
let masterLiveStuds = {};

//create middleware
io.use((socket, next) => {
  const uid = socket.handshake.auth.uid;
  const sid = socket.handshake.auth.sid;

  if(!uid) {
    return next(new Error("no user ID"));
  }
  socket.uid = uid;

  if(!sid) {
    return next(new Error("no scenario ID"));
  }
  socket.sid = sid;
  next();
});


// When a new student/instructor joins, they need to  
//
io.on('connection', socket => {

    // Error handler for middleware.
  socket.on("connect_error", err => {
    console.log("Connnection Error: no user id.")
  });

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
    }
  }

  // if a masterListChat entry for the uid exists, emit it to socket. Otherwise, create an empty entry. 
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

  //  Sockets join rooms immediately after connecting. 
  socket.join(socket.uid); //students join their own room. 
 
  if(socket.uid=="000") { //instructors join everyone else's.
    socket.join("000");
    for(let key in studentList) {
      socket.join(key);

    }
    socket.emit("live students", masterLiveStuds);
  }


  //console.log(io.sockets.adapter.rooms); // This line outputs all rooms and members for debugging. 
  
  // Traffic Alerts: Join, Leave, Message.
  const trafficAlert = (alertType) => {
    let alertString = {};
    alertTime = new Date().toISOString() .replace('T', ' ').replace('Z', ''); // timestamp for event
    if (socket.uid!=="000") { // Sockets belonging to students create alerts for instructor
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


  // send room members message so they can make server-side update
  socket.on("send message", ({messageContents, _to, _from}) => {

  var room = (_to!=="000") ? _to : _from; // room number is student's unique id#
    masterListChats[room].messages.push({               
      contents: messageContents,
      from: _from,
        to: _to,
    });

    // student messages alert instructor
    if(_from!=="000") {
      msg_list = masterListChats[socket.uid].messages;
      trafficAlert("message", {msg_list, room});
    }
    
    alertTime = parseInt(Math.floor(Date.now()/1000));
    console.log(alertTime);

    console.log('++++++++++++++++++++++++++++++++++++++++++')
  


  const group_id = ''
  pool.query('SELECT * FROM SCENARIO_GROUPS', (err, result) => {
    if (err) {
      console.error('Error executing query', err);
    } else {
      group_id = "todo"
    }
  });

    const chatDB_rowEntry = {
      sender: _from,
      recipient:_to,
      message_contents: messageContents,
      timestamp: alertTime,
      sid: socket.sid
      //gid: ....
    }

    const query = 'INSERT INTO chat_history (sender, recipient, message_contents, timestamp, sid, gid) VALUES ($1, $2 ,$3, $4, $5, $6)';
    pool.query(query, chatDB_rowEntry, (err, result) => {
      if (err) {
        console.error('Error executing query', err);
      } else {
        console.log('Query result:', result.rows);
      }
    });



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

console.log(` . . . c h a t . . . `)
console.log(`server listening on port ${process.env.CHAT_SERVER_PORT}`)
io.listen(process.env.CHAT_SERVER_PORT);





    /*
    //practice post

  const postData = JSON.stringify({"hello": "world"});
  const options = {
    // hostname: 'localhost', // default 'localhost'
    port: 5000,
    path: '/api/database',
    method: 'POST', // default 'GET'
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData),
    },
  };
  const req = http.request(options, (res) => {
    console.log(`STATUS: ${res.statusCode}`);
    console.log(`HEADERS: ${JSON.stringify(res.headers)}`);
    res.setEncoding('utf8');
    res.on('data', (chunk) => {
      console.log(`BODY: ${chunk}`);
    });
    res.on('end', () => {
      console.log('No more data in response.');
    });
  });
  req.on('error', (e) => {
    console.error(`problem with request: ${e.message}`);
  });
  // Write data to request body
  req.write(postData);
  req.end();

  */

  