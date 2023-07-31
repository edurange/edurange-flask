import React from 'react';
import OutsideAlerter from "../../utils/outstide-alerter";
import "./chatbox.styles.css";
import GroupClientSocket from "../group_chat_components/group_client_socket/group_client_socket.component";
import SocketEventHandler from "../chat_components/socket_event_handler/socket_event_handler.component";


class Chatbox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
        }
    }

    openChat = () => {
        this.setState({
            open: true,
        });
    }
    closeChat = () => {
        this.setState({
            open: false,
        });
    }

    render() {
       /* open on click, close on click outside */ 
        return (
            <OutsideAlerter callback={this.closeChat}>
                <div className={ this.state.open ? 'edu-chatbox-open' : 'edu-chatbox-closed' } onClick={this.openChat}>
                    <div className="chat_title">
                        <p>chat</p>
                    </div>

                    <div className="socket_container" >
                        <GroupClientSocket uid={this.props.uid} sid={this.props.sid} chat_opened={this.state.open}/>
                    </div>
                </div>
            </OutsideAlerter>
        );
    }
}

export default Chatbox;