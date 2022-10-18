/* Display one chat session.
 */
import "./chat_input.css"

class ChatInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          inputCapture: '',
          message: '',
        };
      }



    render() {
        
        return (

            <div id='chat_input'>
                <form
                    // Emit 'private_message' signal to server. 
                    onSubmit={this.onSubmit}
                    // Don't show the autocomplete menu which collects inputs
                    autoComplete="off"
                >
                    <input
                        type='text'
                        placeholder='. . .'
                        className="chat_input_area"
                        onChange={this.onChange}
                    />
                    <button className='edu-submit' type="submit">
                        send
                    </button>
                </form>
            </div>
            
        );
    }
}

export default ChatInput;