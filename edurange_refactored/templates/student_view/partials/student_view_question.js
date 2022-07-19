import sample_content from './sample_content.json';
import { Guidebox } from './guidebox.js';
let answer = sample_content.StudentGuide.Questions.Question1.Answers.Value;

class Question extends React.Component {

  constructor(props) {
    super(props);
    this.state = { 
      submission: 'unsubmitted'
    }
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

    return (
      <div className="question">
        <h1 className='scenario_name'>{sample_content.ScenarioTitle}</h1>
        <div className="submission-traits">
          <p className="submission-points">{sample_content.StudentGuide.Questions.Question1.Points} points</p>
          <p className="submission-state">{this.state.submission}</p>
        </div>
        <p className="question-text">{sample_content.StudentGuide.Questions.Question1.Text}</p>
        <div class='answer-area'>
          <textarea className="answer" rows="1" cols="50"></textarea><br />
          <button className='submit' type="submit" onClick={this.updateSubmit}>Submit</button>
        </div>
        <Guidebox className='guidebox' />
      </div>
      
    );
  }
}



ReactDOM.render(<Question />, document.getElementById('student_view_question'))