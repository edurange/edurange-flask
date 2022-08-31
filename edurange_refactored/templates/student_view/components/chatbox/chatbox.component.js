import "./chatbox.styles.css"
class Chatbox extends React.Component {
    render() {
        return (
            <div className='edu-chatbox'>
                <p>Chat me up?</p>
                <input className='type_here' type='text' />
            </div>
        );
    }
}

export default Chatbox;