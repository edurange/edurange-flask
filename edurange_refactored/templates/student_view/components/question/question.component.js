import "./question.styles.css"

class Question extends React.Component {

  constructor(props) {
    super(props);

    this.updateSubmit = this.updateSubmit.bind(this);
    this.onChange = this.onChange.bind(this);


    this.state = { 
      submission: 'unsubmitted',
      response: '',
    };

  }

  updateSubmit() {
    this.setState(
      {
        submission: 'submitted',
      }
    )
  }

  onChange(e) {
    this.setState({
      response: e.target.value
    });
  }



  render() {
    const {question} = this.props;
    return (
        <div className='edu-question'>
            <div className="edu-submission-traits">
              <p className="edu-submission-points">- / {question.Points}</p>
              <p className="edu-submission-state">{this.state.submission}</p>
            </div>
            <p className="edu-question-text">{question.Text}</p>
            <div className='edu-answer-area'>
            <input
              className="edu-answer"
              id='name-input'
              onChange={this.onChange}
              value={this.state.response} />
              <button className='edu-submit' type="submit" onClick={this.updateSubmit}><i class="fa fa-check" /></button>
            </div>
        </div>
    );
  }
}



// ReactDOM.render(<Question />, document.getElementById('student_view_question'))
export default Question;