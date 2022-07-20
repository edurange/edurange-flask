import Question from './question.component'
import Reading from './reading.component'
class GuideSection extends React.Component {

    render() {
        // console.log(this.props)
        // return(<div className="student-scenario-section"><h2>This is a section</h2></div>)
        const {section, readings, questions} = this.props;
        const useAltOrder = false; // TODO
        // const { Order } = useAltOrder ? section.AltOrder : section.Order;
        var Order;
        if (!useAltOrder) {
            Order = section.Order
        } else {
            Order = section.AltOrder
        }
        console.log(Order);

        return (
            <div className="student-scenario-section">
              {Order.map(
                (name) => {
                    if (name.includes("Question")) {
                        return(<Question question={questions[name]} key={name}/>);
                    } else {
                        return(<Reading fileName={readings[name]} key={name}/>); // TODO dump reading file contents here and pass string?
                    }
                }
              )}
            </div>
        )
    }
}

export default GuideSection;