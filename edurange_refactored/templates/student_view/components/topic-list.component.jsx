class TopicList extends React.Component {

    render() {
        const {sections} = this.props;
        return (
            <div className='topic_list'>
                <ul>
                    {sections.map(
                        (sec) => {
                            return (<li key={sec.Count}>
                                <a href='student_view'>
                                    {sec.Title}
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