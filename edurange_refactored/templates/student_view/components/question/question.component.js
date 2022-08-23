import "./question.styles.css"

class Question extends React.Component {

  constructor(props) {
    super(props);

    this.updateState = this.updateState.bind(this);
    this.onChange = this.onChange.bind(this);

    this.state = {
      scenarioState:{},
      answer:'',
    };
  }

  componentDidMount() {
    this.setState({scenarioState: this.props.scenarioState});
  }

  updateState(e) {
    var csrf_token = this.props.csrf_token;
    // var csrf_token = csrf_token.split('\"');
    // console.log(csrf_token);
    // console.log(this.props.name.slice(8, 10));

    const requestOptions = {
      method:'POST',
      headers:{'Content-Type':'application/json; charset=UTF-8', 'X-CSRFToken':csrf_token}, 
      body:JSON.stringify({"question":this.props.name.slice(8, 10), "scenario": this.props.scenarioId, "response":this.state.answer}),
    };
    fetch(`/api/post_ans/${this.props.scenarioId}`, requestOptions)
    fetch(`/api/get_state/${this.props.scenarioId}`)
      .then((resp) => resp.json())
      .then((json) => this.setState({scenarioState: json}));
  }

  onChange(e) {
    this.setState({
      answer:(e.target.value),
    });
  }



  render() {
    const {question, scenarioState, name} = this.props;
    console.log(Object.keys(scenarioState.Questions));
    var currentScore;
    var submissionState;
    var submissionStateColor;
    if (name in scenarioState.Questions) {
      currentScore = scenarioState.Questions[name].Score;
      if (currentScore == 0) {
        submissionState = "Incorrect";
        submissionStateColor = {"background-color":"rgba(255,0,0,0.7)"}
      } else if (currentScore > 0 && currentScore < question.Points) {
        submissionState = "In Progress";
        submissionStateColor = {"background-color":"rgba(255,255,0,0.7)"};
      } else {
        submissionState = "Correct";
        submissionStateColor = {"background-color":"rgba(0,128,0,0.7)"}
      }
    } else {
      currentScore = '-';
      submissionState = "Not Attempted";
      submissionStateColor = {"background-color":"rgba(128,128,128,0.7)"}
    }
    return (
        <div className='edu-question'>
            <div className="edu-submission-traits">
              <p className="edu-submission-points">{currentScore} / {question.Points}</p>
              <p className="edu-submission-state" style={submissionStateColor}>{submissionState}</p>
            </div>
            <p className="edu-question-text">{question.Text}</p>
            <div className='edu-answer-area'>
            <input
              type='text'
              className="edu-answer"
              name='edu-answer'
              id='name-input'
              onChange={this.onChange}
              value={this.state.response} />
              <button className='edu-submit' type="submit" onClick={this.updateState}><i className="fa fa-check" /></button>
            </div>
        </div>
    );
  }
}



// ReactDOM.render(<Question />, document.getElementById('student_view_question'))
export default Question;