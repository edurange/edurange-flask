import { appendFile } from "fs";
import { render } from "less";
import studentStates from '../../states.json';
import { useState, useEffect } from "react";
import Student from '../student/student.component';
import usernameList from '../../../../../../edurange-flask/data/tmp/chatnames.json'

import { io } from 'socket.io-client';
const socket = io(`${window.location.hostname}:3001`, {autoConnect:false});

// catch-all listener for development phase
socket.onAny((event, ...args) => {
  console.log(event, args);
});

var i = 0;
var allStudents = [];
var global_msg_list=[];
var newest_msg = "";

/* list of dummy events */
function StudentList({returnSelectedUser}) {
    const [isConnected, setIsConnected] = useState(socket.connected);
    const [currAlert, setCurrAlert] = useState();
    const initStuds = [
        "Marco",
        "Mary",
        "Zebra",
    ];
    const [lastDate, setLastDate] = useState('0');
    const [lastFrom, setLastFrom] = useState();
    const [live, setLive] = useState(initStuds);
    const [uq, setUq] = useState([]);
    const [rq, setRq] = useState(initStuds);
    
    const [inputData, setInputData] = useState("");
    const [selectedStudent, setSelectedStudent] = useState();
    const [newMessage, setNewMessage] = useState(null);

    const usernames = usernameList;

    const statesLen = Object.keys(studentStates).length;

    // gathering student user ID / username list

  useEffect(() => {
    const uid = "000";
    socket.auth = { uid }
    socket.connect();

    socket.on('connect', () => {
      console.log("instructor has connected.");
    });

    socket.emit("instructor connected");

    socket.on("alert", (_alert) => {
        //console.log(`alert : ${JSON.stringify(_alert)}`);
        onRecvAlert(_alert);
    });

    socket.on("new message", ({messageContents, _to, _from, room}) => {
        socket.emit("request msg_list", {messageContents, _to, _from, room});
    });

    socket.on("msg_list update", ({msg_list, room}) => {
        global_msg_list = msg_list;
        setNewMessage(msg_list[msg_list.length - 1]);
        newest_msg = global_msg_list[global_msg_list.length - 1];

        let stud;
        for(let i = 0; i < allStudents.length; i++){
            if (allStudents[i]["uid"] == room) {
                allStudents[i]["messages"] = msg_list;    
            }
        }
    });

    const findStudent = (selStud) => {
        for(let i in allStudents) {
            if (allStudents[i][id] == selStud) {
                return allStudents[i];
           }
        }
        return null;
    };

    const listener = event => {
        if (event.code === "Enter" || event.code === "NumpadEnter") {
            console.log("enter pressed...");
          event.preventDefault();
          
          if(inputData && selectedStudent) {
            const recipient = findStudent(selectedStudent)
            socket.emit("send message", {messageContents: inputData, to: recipient["uid"], from: "000"});
            setInputData("");
        } else if (inputData && !selectedStudent) { 
            console.log("input data, no selectedStudent");
        } else if (!inputData && selectedStudent) {
            console.log("selectedStudent, no inputData");
        } else {
            console.log("no input data, no selectedStudent");
        }
        }
    };

    
  
    document.addEventListener("keydown", listener);
  
    return () => {
      socket.off('connect');
      socket.off('alert');
      socket.off("new message");
      socket.off("send message");
      socket.off("msg_list update");
      document.removeEventListener("keydown", listener);
    };
  }, []);

    const onRecvAlert = (_alert) => {
        // Add id key.
        _alert["id"] = usernames[_alert["uid"] - 1]; // user1 has a uid of 2.
        allStudents.push(_alert);
        console.log(`all students now contains ${JSON.stringify(allStudents)}}`)
        handleEvent(_alert);
    }


/* Contains the list of chat sessions and the 'Everyone' chat session.
 * Represent the chat sessions as: 
 * 'Everyone' is always at the top
 * Students are displayed in a queue which is updated based on students
 *      entering the chat session and new messages.
 *      Each student that is popped from the queue is re-pushed immediately.
 */ 
    const isNewer = (date1, date2) =>  {
        return date1 > date2;
    }

    const removeFromRq = (stud) => {
        let newRq = [...rq]
        var idx = newRq.indexOf(stud)
        if (idx >= 0) {
            newRq.splice(idx, 1);
            return (true, newRq)
        }
        return (false, newRq);
    }

    const removeFromUq = (stud) => {
        let newUq = [...uq]
        var idx = newUq.indexOf(stud)
        if (idx >= 0) {
            newUq.splice(idx, 1);
            return (true, newUq)
        }
        return (false, newUq)
    }
 
    const newUnread = (from) => {
        /* remove student from rq and push to uq */
        if (!uq?.includes(from)) {
            let newUq = removeFromUq(from);
            newUq.push(from)
            setUq(newUq)
        }
        let newRq = removeFromRq(from);
        setRq(newRq)
    }

    const newJoined = (stud) => {
        let newRq = [...rq]
        /* if student not in one of the queues, add to read queue */
        if (!rq?.includes(stud) && !uq?.includes(stud)) {
            newRq.push(stud);
            setRq(newRq);
        }
    }

    const chatOnClick = (stud) => {
        /* remove stud from both lists if in them, 
         * set current stud to stud
         *  push to readq
         */
        /* remove student from rq and push to uq */
        /* remove from uq regardless, append*/
        let changedRq, newRq = removeFromRq(stud);
        let changedUq, newUq = removeFromUq(stud);
        newRq.push(stud)
        setRq(newRq)
        setUq(newUq)

        // set as intended recipient for message
        setSelectedStudent(stud);
        let selectedUser;
            for(let i = 0; i < allStudents.length; i++){
                if (allStudents[i]["id"] == stud) {
                    selectedUser = allStudents[i];    
               }
            }
        if(selectedUser) {
            returnSelectedUser(selectedUser);    
        }
    }
    
    const handleEvent = (e) => {
        console.log(`value of e : ${JSON.stringify(e)}`)
        var newDate = e["time"]
        console.assert(newDate != null)
        switch (e["type"]) {
            case "message":
                console.log(`message from: ${e["from"]}, to ${e["to"]}`)
                newUnread(e["from"]);
                break;
            case "studJoin":
                console.log(`student ${e["id"]} joined`)
                newJoined(e["id"])
                if (isNewer(newDate, lastDate)) {
                    setLastDate(newDate);
                    setLive(e["live"])
                }
                break;
            case "studLeave":
                console.log(`student ${e["id"]} left`)
                if (isNewer(newDate, lastDate)) {
                    setLastDate(newDate);
                    setLive(e["live"])
                }
                break;
        }
        console.log(`lastDate: ${lastDate}, liveStuds: ${live}`)
    }

    const msgOnClick = () => {
        if (i < statesLen) {
            var e = studentStates[i.toString()]
            ++i
            console.assert(e != null)
            handleEvent(e);
        }
    }

    const onChange = (e) => {
        setInputData(e.target.value);
      }
    
    const onFormSubmit = e => {
        e.preventDefault();
        if(inputData && selectedStudent) {
            let recipient;
            for(let i = 0; i < allStudents.length; i++){
                if (allStudents[i]["id"] == selectedStudent) {
                    recipient = allStudents[i];    
               }
            }
            if(recipient) {
                socket.emit("send message", {messageContents: inputData, _to: recipient["uid"], _from: "000"});
            } else {
                console.log("recipient is null");
            }
            setInputData("");
        } else if (inputData && !selectedStudent) { 
            console.log("input data, no selectedStudent");
        } else if (!inputData && selectedStudent) {
            console.log("selectedStudent, no inputData");
        } else {
            console.log("no input data, no selectedStudent");
        }
    }
    
    
    
    return (
        <div id="studentList" className="list-group w-25 overflow-auto">
        
        <div className='instructor-chat-input-area'>
            <form
              onSubmit={ onFormSubmit }
              autoComplete="off"
            >
              <input
                type='text'
                className="instructor-chat-input-box"
                autoComplete='off'
                onChange={ onChange }
                value= {inputData}
              />
              <button
                type="submit"
              >
              Send
              </button>

            </form>
        </div>

        <p>{JSON.stringify(newMessage) || "newest message"}</p>
            <button onClick={msgOnClick}>
            Click Me
            </button>
            {uq?.map((stud) => {
                return(
                    <Student 
                        key={stud} 
                        name={stud} 
                        status="unread" 
                        onClick={chatOnClick} 
                        isLive={live?.includes(stud)}/>
                )
            })}
            {rq?.map((stud) => {
                return(
                    <Student 
                    key={stud} 
                    name={stud} 
                    status="read" 
                    onClick={chatOnClick}
                    isLive={live?.includes(stud)}/>
                )
            })}
        

        </div>
    )
}

export default StudentList;