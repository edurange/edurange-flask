import "./question.styles.css"

class Question extends React.Component {

  constructor(props) {
    super(props);
    this.updateState = this.updateState.bind(this);
    this.onChange = this.onChange.bind(this);

    this.state = {
      qstate: Question.QUESTION_STATE.Unsubmitted,
      currentScore: '-',
      scenarioState:{},
      answer:'',
    };
  }

  // Set up initial state of question
  componentDidMount() {
    const {question, scenarioState, name} = this.props;
    if (!(name in scenarioState.Questions)) {
      this.setState({scenarioState});
    } else if (scenarioState.Questions[name].Score == question.Points) {
      this.setState({
        scenarioState, 
        qstate: Question.QUESTION_STATE.Completed,
        currentScore: question.Points.toString(),
      });
    } else {
      this.setState({
        scenarioState, 
        qstate: Question.QUESTION_STATE.Submitted,
        currentScore: scenarioState.Questions[name].Score.toString(),
      })
    }
  }

  updateState(e) {
    e.preventDefault();
    var csrf_token = this.props.csrf_token;
    const { Unsubmitted, Submitted, Incorrect, Correct, Completed } = Question.QUESTION_STATE;
    var qstate;
    const requestOptions = {
      method:'POST',
      headers:{'Content-Type':'application/json; charset=UTF-8', 'X-CSRFToken':csrf_token}, 
      body:JSON.stringify({"question":this.props.name, "scenario": this.props.scenarioId, "response":this.state.answer}),
    };
    fetch(`/api/post_ans/${this.props.scenarioId}`, requestOptions)
      .then((_) => {
        fetch(`/api/get_state/${this.props.scenarioId}`)
          .then((resp) => resp.json())
          .then((scenarioState) => {
            if (this.state.qstate == Completed) {
              qstate = Completed;
            } else if (!(this.props.name) in scenarioState.Questions) {
              qstate = Unsubmitted;
              // bug? TODO
              return;
            } else if (scenarioState.Questions[this.props.name].Correct != true) {
              qstate = Incorrect;
            } else {
              qstate = Correct;
            }
            this.setState({currentScore: scenarioState.Questions[this.props.name].Score, scenarioState, qstate});
          });
        });
  }

  onChange(e) {
    this.setState({
      answer:(e.target.value),
    });
  }

  _onKeyDown = (e) => {
    if (e.key === 'Enter') {
      this.updateState(e);
    }
  }

  static QUESTION_STATE = {
    Unsubmitted: 0, // -/20 <- question number not a key into state object
    Submitted:   1, // 10/20 and no checkmark <- 
    Incorrect:   2, // */20 and x-mark goes away on refresh
    Correct:     3, // 10/20 and checkmark goes away on refresh
    Completed:   4, // 20/20 and checkmark, never reverts
  }

  renderSubmissionState() {
    var cssclass, icon, text;
    switch (this.state.qstate) {
      case Question.QUESTION_STATE.Unsubmitted:
        cssclass = "unsubmitted";
        icon = null
        text = "unsubmitted"
        break;
      case Question.QUESTION_STATE.Submitted:
        cssclass = "submitted";
        icon = null
        text = "incomplete";
        break;
      case Question.QUESTION_STATE.Incorrect:
        cssclass = "incorrect";
        icon = (<i className="fa-solid fa-circle-xmark" />);
        text = "incorrect";
        break;
      case Question.QUESTION_STATE.Correct:
        cssclass = "correct";
        icon = (<i className="fa-solid fa-circle-check" />);
        text = "correct";
        break;
      default: // Completed
        cssclass = "completed";
        icon = (<i className="fa-solid fa-circle-check" />);
        text = "completed";
        break;
    }
    return (
      <p className={`edu-submission-state ${cssclass}`}>
        {text}
        {icon}
      </p>
    );
  }

  render() {
    const {question, scenarioState, name} = this.props;
    return (
        <div className='edu-question'>
            <div className="edu-submission-traits">
              <p className="edu-submission-points">{this.state.currentScore} / {question.Points}</p>
              {this.renderSubmissionState()}
            </div>
            <p className="edu-question-text">{question.Text}</p>
            <div className='edu-answer-area'>
            <form
              onSubmit={this.updateState}
              autocomplete="off"
            >
            <input
              type='text'
              className="edu-answer"
              name='edu-answer'
              id='name-input'
              onChange={this.onChange}
              value={this.state.response} />
              <button className='edu-submit' type="submit"><i className="fa-solid fa-check" /></button>
            </form>
            </div>
        </div>
    );
  }
}

export default Question;