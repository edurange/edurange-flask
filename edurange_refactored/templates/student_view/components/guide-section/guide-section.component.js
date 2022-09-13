import React from 'react';
import Question from '../question/question.component'
import Reading from '../reading/reading.component'
import "./guide-section.styles.css"
class GuideSection extends React.Component {

    render() {
        const {section, readings, questions, scenarioState, scenarioId, csrf_token} = this.props;
        // If the instructor has given you an alternative order, determine whether to use it.
        // TODO: Add a variable for the instructor to set so that they can activate the alt order.
        const useAltOrder = false;  
        var Order;
        if (!useAltOrder) {
            Order = section.Order
        } else {
            Order = section.AltOrder
        }

        return (
            <div className="student-scenario-section">
              {Order.map(
                // Order is made up of pairs, eg. ['r', '1'], ['q', '1'], ['r', '2']
                // that determine the order that the questions and readings should appear on the
                // page. So in that example, 'reading 1' would be rendered first, then 'question 1',
                // then 'reading 2'. React requires a unique key to determine when to re-render each
                // component. Create this key by appending the two items in the ordered pair, e.g.
                // 'r1', 'q1', 'r2'.
                (pair) => {
                    if (pair[0] == 'q') {
                        return(
                            <Question qid={pair[1]} 
                                    question={questions[pair[1]]} 
                                    key={pair[0]+pair[1]} 
                                    scenarioState={scenarioState} 
                                    scenarioId={scenarioId} 
                                    csrf_token={csrf_token} />
                        );
                    } else {
                        return(<Reading reading={readings[pair[1]]} key={pair[0]+pair[1]}/>); 
                    }
                }
              )}
            </div>
        )
    }
}

export default GuideSection;