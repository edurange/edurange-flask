/* This is the entry point for the instructor view and 
 * the super container for the other components.
 */ 
import Student from "../student/student.component";
import "./instructor_view.css";
import ChatWindow from "../chat_window/chat_window.component";
import {createRoot} from 'react-dom/client';

class InstructorView extends React.Component {
    render () {
        
        return (
            <div id="instructor_view">
                <Student />
                <ChatWindow />
            </div>
        );
    }
}

var e = document.getElementById('instructor_view');
const root=createRoot(e);

root.render(<InstructorView />);