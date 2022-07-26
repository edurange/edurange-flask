import "./question.styles.css"

class Question extends React.Component {

  constructor(props) {
    super(props);
    this.state = { 
      submission: 'unsubmitted'
    };
    this.updateSubmit = this.updateSubmit.bind(this);
  }

  updateSubmit() {
    this.setState(
      {
        submission: 'submitted'
      }
    )
  }



  render() {
    const {question} = this.props;
    return (
        <div className='edu-question'>
            <div className="edu-submission-traits">
              <p className="edu-submission-points">{question.Points} points</p>
              <p className="edu-submission-state">{this.state.submission}</p>
            </div>
            <p className="edu-question-text">{question.Text}</p>
            <div className='edu-answer-area'>
              <textarea className="edu-answer" rows="1" cols="50"></textarea><br />
              <button className='edu-submit' type="submit" onClick={this.updateSubmit}>Submit</button>
            </div>
        </div>
    );
  }
}



// ReactDOM.render(<Question />, document.getElementById('student_view_question'))
export default Question;