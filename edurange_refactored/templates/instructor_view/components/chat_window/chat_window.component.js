/* Display one chat session.
 */
import "./chat_window.css"
import ChatMessageSection from "../chat_message_section/chat_message_section.component";

class ChatWindow extends React.Component {
    render() {
        const user = this.props;
        return (
            <div id='chat'>
                <ChatMessageSection user={user}/>
            </div>
        );
    }
}

export default ChatWindow;