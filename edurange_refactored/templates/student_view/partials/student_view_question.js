'use strict';
import sample_content from './sample_content.json';
console.log(sample_content);
let submission = 'unsubmitted';
let answer = sample_content.StudentGuide.Questions.Question1.Answers.Value;

class Question extends React.Component {

  render() {

    return (
      <div className="question">
        <h1 className='scenario_name'>{sample_content.ScenarioTitle}</h1>
        <form className="question--form">
                  <div className="submission-traits">
                      <p className="submission-points">{sample_content.StudentGuide.Questions.Question1.Points} points</p>
                      <p className="submission-state">{submission}</p>
                  </div>
          <p className="question-text">{sample_content.StudentGuide.Questions.Question1.Text}</p>


          <textarea className="answer" rows="1" cols="50"></textarea><br />
          <input className='submit' type="submit" value="Submit" />
        </form>
        <div className="guide">
          <ul className="guide_list">
            <li>Number of Questions: {sample_content.StudentGuide.TotalQuestions}</li>
            <li>Number of Points: {sample_content.StudentGuide.TotalPoints}</li>
          </ul>
        </div>
      </div>
      
    );
  }
}

ReactDOM.render(<Question />, document.getElementById('student_view_question'))