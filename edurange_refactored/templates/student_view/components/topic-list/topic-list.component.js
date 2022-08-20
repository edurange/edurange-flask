import "./topic-list.styles.css"
class TopicList extends React.Component {

    render() {
        const {sections} = this.props;
        return (
            <div className='edu-topic-list'>
                <ul>
                    {sections.map(
                        (sec) => {
                            return (<li key={sec.Count}>
                                <a href='student_view'>
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