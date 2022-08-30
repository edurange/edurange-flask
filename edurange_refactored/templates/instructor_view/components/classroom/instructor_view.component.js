import Student from "../student/student.component";
import "./instructor_view.css";
import Chat from "../chat/chat.component";

class InstructorView extends React.Component {
    render () {
        return (
            <div id="instructor_view">
                <Student />
                <Chat />
            </div>
        );
    }
}

var e = document.getElementById('instructor_view');
ReactDOM.render(<InstructorView />, e);