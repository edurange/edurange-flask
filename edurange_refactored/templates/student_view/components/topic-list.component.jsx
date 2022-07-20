class TopicList extends React.Component {

    render() {
        const {sections} = this.props;
        return (
            <div className='topic_list'>
                <ul>
                    {sections.map(
                        (sec) => {
                            return (<li>
                                <a href='student_view'>
                                    {sec.Title}
                                </a>
                            </li>)
                        }
                    )}
                    <li><a href='student_view'>Topic A</a></li>
                    <li><a href='student_view'>Topic B</a></li>
                    <li><a href='student_view'>Topic C</a></li>
                    <li><a href='student_view'>Topic D</a></li>
                </ul>
            </div>
        );
    }
}

export default TopicList;