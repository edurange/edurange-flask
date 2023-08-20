import React from 'react';
import "./question.styles.css"

class Question extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      qstate: Question.QUESTION_STATE.Unsubmitted,
      currentScore: '-',
      scenarioState:{},
      answer:'',
    };
  }

  // Set up initial state of question
  componentDidMount() {
    const {question, scenarioState, qid} = this.props;
    if (!(qid in scenarioState.Questions)) {
      this.setState({scenarioState});
    } else if (scenarioState.Questions[qid].Score == question.Points) {
      this.setState({
        scenarioState, 
        qstate: Question.QUESTION_STATE.Completed,
        currentScore: question.Points.toString(),
      });
    } else {
      this.setState({
        scenarioState, 
        qstate: Question.QUESTION_STATE.Submitted,
        currentScore: scenarioState.Questions[qid].Score.toString(),
      })
    }
  }


  // Post an answer to the back end. Fetch the new state 
  // and re-render the question to show the result.
  onSubmit = (e) => {
    const {qid, csrf_token, scenarioId} = this.props;
    // Prevent the form from posting to the front-end by default
    e.preventDefault();
    const { Unsubmitted, Submitted, Incorrect, Correct, Completed } = Question.QUESTION_STATE;
    var qstate;
    const requestOptions = {
      method:'POST',
      headers:{'Content-Type':'application/json; charset=UTF-8', 'X-CSRFToken':csrf_token}, 
      body:JSON.stringify({"question": qid, "scenario": scenarioId, "response":this.state.answer}),
    };
    // POST and only after we've posted, GET the current state from the back end
    fetch(`/api/post_ans/${scenarioId}`, requestOptions)
      .then((_) => {
        fetch(`/api/get_state/${scenarioId}`)
          .then((resp) => resp.json())
          .then((scenarioState) => {
            if (this.state.qstate == Completed) {
              qstate = Completed;
            } else if (!(qid) in scenarioState.Questions) {
              qstate = Unsubmitted;
              return;
            } else if (scenarioState.Questions[qid].Correct == false) {
              qstate = Incorrect;
            } else {
              qstate = Correct;
            }
            this.setState({currentScore: scenarioState.Questions[qid].Score, scenarioState, qstate});
          });
        });
  }

  // Save what the student has entered in the text box.
  onChange = (e) => {
    this.setState({
      answer:(e.target.value),
    });
  }

  static QUESTION_STATE = {
    Unsubmitted: 0, // -/20 <- question number not a key into state object
    Submitted:   1, // 10/20 and no checkmark <- 
    Incorrect:   2, // */20 and x-mark goes away on refresh
    Correct:     3, // 10/20 and checkmark goes away on refresh
    Completed:   4, // 20/20 and checkmark, never reverts
  }

  renderSubmissionState = () => {
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
    const {question} = this.props;
    return (
        <div className='edu-question'>
            <div className="edu-submission-traits">
              <p className="edu-submission-points">{this.state.currentScore} / {question.Points}</p>
              {this.renderSubmissionState()}
            </div>
            <p className="edu-question-text">{question.Text}</p>
            <div className='edu-answer-area'>
            <form
              // POST answer and GET new state
              onSubmit={this.onSubmit}
              // Don't show the autocomplete menu which collects answers for all questions
              autoComplete="off"
            >
            <input
              type='text'
              className="edu-answer"
              name='edu-answer'
              id='name-input'
              onChange={this.onChange}
            />
              <button className='edu-submit' type="submit"><i className="fa-solid fa-check" /></button>
            </form>
            </div>
        </div>
    );
  }
}

export default Question;