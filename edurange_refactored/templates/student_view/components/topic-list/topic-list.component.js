import "./topic-list.styles.css"
class TopicList extends React.Component {

    render() {
        const {sections, setState, currentSection} = this.props;
        return (
            <div className='edu-topic-list'>
                <ul>
                    {sections.map(
                        (sec) => {
                            return (<li key={sec.Count}>
                                <a id={sec.Count - 1 === currentSection ? 'topic-current' : 'topic'} onClick={() => {setState({currentSection: sec.Count - 1})}}>
                                    <div id='topicNumber'>{sec.Count}</div><div id='topicName'>{sec.Title}</div>
                                </a>
                            </li>)
                        }
                    )}
                </ul>
            </div>
        );
    }
}

export default TopicList;