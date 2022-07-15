'use strict';

class Question extends React.Component {
  
  render() {
    return (
      <div className="question">
        <form className="question--form">
                  <div class="submission-traits">
                      <p class="submission-points">8 points</p>
                      <p class="submission-state">unsubmitted</p>
                  </div>
          <p class="question-text">There is one chopstick between each philosopher, to their immediate right and left. <br />
          In order to eat, a given philosopher needs to use both chopsticks. <br />
          How can you ensure all the philosophers can eat reliably without starving to death?</p>


          <textarea className="answer" rows="1" cols="50"></textarea><br />
          <input className='submit' type="submit" value="Submit" />
        </form>
        <div class="guide">
          <p class="text-box">Guide box here</p>
        </div>
      </div>
      
    );
  }
}

ReactDOM.render(<Question />, document.getElementById('student_view_question'))