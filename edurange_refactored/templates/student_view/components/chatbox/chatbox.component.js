import React from 'react';
import OutsideAlerter from "../../utils/outstide-alerter";
import "./chatbox.styles.css"
import ClientSocket from "../client_socket/client_socket.component"
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
                    <p>instructor chat</p>
                    <ClientSocket sid= {this.props.sid} uid={this.props.uid} chat_opened={this.state.open}/>
                </div>
            </OutsideAlerter>
        );
    }
}

export default Chatbox;


/*

*/