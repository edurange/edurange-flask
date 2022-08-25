import Question from '../question/question.component'
import Reading from '../reading/reading.component'
import "./guide-section.styles.css"
class GuideSection extends React.Component {

    render() {
        // console.log(this.props)
        // return(<div className="student-scenario-section"><h2>This is a section</h2></div>)
        const {section, readings, questions, scenarioState, csrf_token} = this.props;
        const useAltOrder = false; // TODO
        // const { Order } = useAltOrder ? section.AltOrder : section.Order;
        var Order;
        if (!useAltOrder) {
            Order = section.Order
        } else {
            Order = section.AltOrder
        }

        return (
            <div className="student-scenario-section">
              {Order.map(
                (item) => {
                    if (item[0] == 'q') {
                        return(<Question name={item[1]} question={questions[item[1]]} key={item[1]} scenarioState={scenarioState} scenarioId={this.props.scenarioId} csrf_token={this.props.csrf_token} />);
                    } else {
                        return(<Reading reading={readings[item[1]]} key={item[1]}/>); // TODO dump reading file contents here and pass string?
                    }
                }
              )}
            </div>
        )
    }
}

export default GuideSection;