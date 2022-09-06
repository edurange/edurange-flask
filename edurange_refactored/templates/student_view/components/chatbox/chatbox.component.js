import OutsideAlerter from "../../utils/outstide-alerter";
import "./chatbox.styles.css"
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
                    <p>Chat me up?</p>
                    <input className='type_here' type='text' />
                </div>
            </OutsideAlerter>
        );
    }
}

export default Chatbox;