/* Display one chat session.
 */
import io from 'socket.io-client';
import "./chat_message_section.css"
import ChatEntry from "../chat_entry/chat_entry.component";
// import ChatInput from "../chat_input/chat_input.component";

class ChatMessageSection extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        //    user: null,
           messages: ["Hello", "Hi"],
        };
    }

    componentDidMount() {
        // this.state.user = this.props;
        // this.state.messages = this.state.user.messages;
        this.state.messages = ["Hello", "Hi"];
    }

    render() {
        console.log(this.state.messages);
        function getMessagesContent(messages) {
            let content = [];
            for (let i = 0; i < messages.length; i++) {
                const item = messages[i];
                content.push(<p key={i}>{item}</p>);
            }
            return content;
        };
        console.log(getMessagesContent(this.state.messages));
        return(
            <div>
                {getMessagesContent(this.state.messages)}
            </div>
        );
    }
}

export default ChatMessageSection;