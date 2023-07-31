// Creating a new server from socket io
const { Server } = require("socket.io");

// Node-Postgres library, for retrieving and inserting database information
const pg = require('pg');
const dot_env_module = require('dotenv').config();
const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });

// Creating an application to handle communiction, using the express framework
const express = require("express"); 
const app = express();

// Employing the use of cross-origin-resource-sharing (CORS), to allow
// communication between this node server, and the one that deploys flask. 
const cors = require("cors");
app.use(cors());

// Create an http.Server instance from the express app
const http = require('http'); // Import the http module
const server = http.createServer(app);

// Define server instance, with CORS policy. 
const io = new Server(server, {
    cors: {
        // Websocket might be using ports 443 and 80 for traffic
        // To Do: Figure out appropriate Cors Rules
        origin: [ "https://" + process.env.HOST_EXTERN_ADDRESS  + ":5000",
        "http://" + process.env.HOST_EXTERN_ADDRESS  + ":5000",
        "https://" + process.env.HOST_EXTERN_ADDRESS  + ":443",
        "http://" + process.env.HOST_EXTERN_ADDRESS  + ":80",
        "https://" + process.env.HOST_EXTERN_ADDRESS  + ":3001",
        "http://" + process.env.HOST_EXTERN_ADDRESS  + ":3001",
      ],
    transports: ["websocket"],
    },
    //allowEIO3: true,
    //allowEIO4: true,
});

// Middleware. This is information passed during the initial handshake. 
io.use((socket, next) => {
    
    const uid = socket.handshake.auth.uid;
    const sid = socket.handshake.auth.sid;
    
    const is_instructor = socket.handshake.auth.is_instructor;

    // Middleware forms a processing chain, returning the "next" process in the chain.
    if (!uid || !sid || !is_instructor) {
        return next(new Error("UID, SID, or Instructor Authentication missing."))
    }

    socket.uid = uid;
    socket.sid = sid;

    // Assign roles to sockets
    socket.instructor = is_instructor;
    socket.student = !is_instructor;
     
    next();
})


// Once connected, these functions are registered. 
io.on("connection", (socket) => {

    console.log("connected!")

    //---------------------------------------------//
    // Reusable query functions
    const queryError = (err) => {
        if(err) { console.error('Error executing query.', err) }
    }

    async function insertIntoChatHistory(row) {
        const insertQuery = 'INSERT INTO chat_history (sender, recipient, message_contents, timestamp, sid) VALUES ($1, $2 ,$3, $4, $5)';
        pool.query(insertQuery, row, (err, result) => { queryError(err); });
    }
    
    // Pull previous chat information
    async function retrieveChatHistory() {
        try {
            const previous_chat_query = 'SELECT * FROM chat_history WHERE (sender=$1 OR recipient=$1) AND sid=$2'
            const result = await pool.query(previous_chat_query, [socket.uid, socket.sid]);
            return result;
            } 
        /*
            Todo:
            Does this account for empty chats?
            Do we need to do result.rows?
            Do we need to reformat the information?
        */
        catch (err) {
          console.error('Error executing query:', err);
        }
        return;
    }

    async function retrieveStudentList() {
        try {
            
            const gid_query = 'SELECT group_id FROM scenario_groups WHERE scenario_id=$1'
            const gid = await pool.query(gid_query, [socket.sid]);
            
            const student_list_query = 'SELECT user_id FROM group_users WHERE group_id=$1'
            const result = await pool.query(student_list_query, [gid]);
            
            return result
            } 
        /*
            Todo:
            Does the instructor have an sid?
            Does asking for group_id directly work okay?
            Do we need to reformat the information?
        */
        catch (err) {
          console.error('Error executing query:', err);
        }
        return;
    }
    //---------------------------------------------//

    const previousChat = retrieveChatHistory();
    console.log(`Previous Chat: ${previousChat}`); /*TESTING*/

    const studentList = retrieveStudentList();
    console.log(`Student List: ${studentList}`); /*TESTING*/

    if(socket.instructor) {
        studentList.forEach(student => {
            //each student is ideally a row object
            //group_users is id, user_id, and group_id
            //student[1]
            socket.join(student); 
            //studentList should have returns an array of studentIDs
            //and the instructor can join a room for each
        });
    }

    //----------------------------------------------//
    //  Socket Events //

    // Error handler for middleware.
    socket.on("connect_error", err => {
        console.log("Connnection Error: missing user id or scenario id.")
    });

    // Once instructor joins, students can send messages.
    if(socket.instructor) {
        io.emit("instructor live", socket.uid);
    }

    socket.on("send button pressed", ({message, recipient}) => {
        
        const room = socket.student ? socket.uid : recipient;
        io.to(room).emit("new message", {message});

        const timestamp = new Date().toISOString().replace('T', ' ').replace('Z', '');
        
        // The database accepts values in the format : [sender, recipient, message_contents, timestamp, sid]
        database_values = [socket.uid, recipient, message, timestamp, socket.sid]
    
    });

    socket.on("disconnect", () => {
        alert = socket.is_instructor ? "instructor disconnected" : "student disconnected";
        io.emit(alert);
    });
    
});

io.listen(3001);
console.log("listening");