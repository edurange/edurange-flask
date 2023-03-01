/* Display one chat entry.*/
import "./chat_entry.css"
class ChatEntry extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const {message, fromSelf, user} = this.props;
        // determine value of message div className
        const messageType = fromSelf ? 'fromSelf' : 'fromOther'; 
        
        return (
            <div className='messageContainer'>
                <div className='userID' id={messageType}>
                    {user}
                </div>
                <div className={messageType}>
                    {message}
                </div>
            </div> /* end display one chat entry */
        );
    }
}

export default ChatEntry;