class GuideSection extends React.Component {

    render() {
        const {section, readings, questions} = this.props;
        const useAltOrder = false; // TODO
        const { Order } = useAltOrder ? section.AltOrder : section.Order;
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