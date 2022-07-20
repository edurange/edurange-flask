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
        <div className='question'>
            <div className="submission-traits">
            <p className="submission-points">{question.Points} points</p>
            <p className="submission-state">{this.state.submission}</p>
            </div>
            <p className="question-text">{question.Text}</p>
            <div className='answer-area'>
            <textarea className="answer" rows="1" cols="50"></textarea><br />
            <button className='submit' type="submit" onClick={this.updateSubmit}>Submit</button>
            </div>
        </div>
    );
  }
}



// ReactDOM.render(<Question />, document.getElementById('student_view_question'))
export default Question;