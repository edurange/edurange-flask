import { appendFile } from "fs";
import { render } from "less";
import studentStates from '../../states.json';
import { useState, useEffect } from "react";
import Student from '../student/student.component';
import usernameList from '../../../../../../edurange-flask/data/tmp/chatnames.json'
 
 
 
 
 
var i = 0;
 
/* list of dummy events */
function StudentList({returnSelectedUser, alert}) {
    
   const initStuds = ["Marco","Mary","Zebra",];
   const [selectedStudent, setSelectedStudent] = useState();
   const [lastDate, setLastDate] = useState('0');
   const [lastFrom, setLastFrom] = useState();
   const [live, setLive] = useState(initStuds);
   const [uq, setUq] = useState([]);
   const [rq, setRq] = useState(Object.values(usernameList));
   const usernames = usernameList;
 
   const statesLen = Object.keys(studentStates).length;
 
   // gathering student user ID / username list
 
 useEffect(()=>{
    if(alert) {
        handleEvent(alert);
    }
 }, [alert]);
 
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
       let newRq = [...rq];
       var idx = newRq.indexOf(stud);
       if (idx >= 0) {
           newRq.splice(idx, 1);
           return (true, newRq);
       }
       return (false, newRq);
   }
 
   const removeFromUq = (stud) => {
       let newUq = [...uq];
       var idx = newUq.indexOf(stud);
       if (idx >= 0) {
           newUq.splice(idx, 1);
           return (true, newUq);
       }
       return (false, newUq);
   }
   const newUnread = (from) => {
       /* remove student from rq and push to uq */
       if (!uq?.includes(from)) {
           let newUq = removeFromUq(from); //ASK LEVI: remove from rq?
           newUq.push(from)
           setUq(newUq)
       }
       let newRq = removeFromRq(from);
       setRq(newRq);
   }
 
   const newJoined = (stud) => {
       let newRq = [...rq]
       /* if student not in one of the queues, add to read queue */
       if (!rq?.includes(stud) && !uq?.includes(stud)) {
           newRq.push(stud);
           setRq(newRq);
       }
   }

   const newLive = (stud) => {
    let newLive = [...live]
    /* if student not in one of the queues, add to read queue */
    if (!live?.includes(stud)) {
        newLive.push(stud);
        setLive(newLive);
    }
   }

   const removeLive = (stud) => {
    let newLive = [...live]
    /* if student not in one of the queues, add to read queue */
    if (live?.includes(stud)) {
        newLive.splice(live.indexOf(stud),1);
        setLive(newLive);
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

       // pass this user to parent, instructor view
       returnSelectedUser(stud);

       // set state to pass as props for Student component.
       setSelectedStudent(stud);
   }
  
   const handleEvent = (e) => {
       //console.log(`value of e : ${JSON.stringify(e)}`)
       var newDate = e["time"]
       console.assert(newDate != null)
       switch (e["type"]) {
        case "message":
           case "message":
               //console.log(`message from: ${e["from"]}, to ${e["to"]}`)
               newUnread(e["id"]);
               break;
           case "studJoin":
               console.log(`student ${e["id"]} joined`)
               newJoined(e["id"])
               if (isNewer(newDate, lastDate)) {
                   setLastDate(newDate);
                   newLive(e["id"]);
               }
               break;
           case "studLeave":
               console.log(`student ${e["id"]} left`)
               if (isNewer(newDate, lastDate)) {
                   setLastDate(newDate);
                   removeLive(e["id"]);
               }
               break;
       }
       //console.log(`lastDate: ${lastDate}, liveStuds: ${live}`)
   }
 
   const msgOnClick = () => {
       if (i < statesLen) {
           var e = studentStates[i.toString()]
           ++i
           console.assert(e != null)
           handleEvent(e);
       }
   }
  
   return (
       <div id="studentList" className="list-group w-25 overflow-auto">
        
           {uq?.map((stud) => {
               return(
                    <Student
                        selectedStudent={selectedStudent}
                        key={stud}
                        name={stud}
                        status="unread"
                        onClick={chatOnClick}
                        isLive={live?.includes(stud)}
                    />
               )
           })}
           {rq?.map((stud) => {
               return(
                    <Student
                        selectedStudent={selectedStudent}
                        key={stud}
                        name={stud}
                        status="read"
                        onClick={chatOnClick}
                        isLive={live?.includes(stud)}
                    />
               )
           })}
 
       </div>
   )
}
 
export default StudentList;

