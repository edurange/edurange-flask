/* Display a student in the student_list. Attributes:
 * isEveryone - bool
 * hasNew - bool
 * studentName
 * currentScore
 */
import "./student.css"

function Student(props) {
    const isLive = true;
    var className = "list-group-item list-group-item-action d-flex justify-content-between"
    if (!props.isLive) {
        className += " list-group-item-secondary"
    }
    return (
        <button 
            type="button" 
            id='student' 
            className={className} 
            onClick={() => props.onClick(props.name)}>
                {props.name}
                <div>
                {props.status == "unread" && 
                    <span>New</span>
                }
                </div>
        </button>
    );
}

export default Student;