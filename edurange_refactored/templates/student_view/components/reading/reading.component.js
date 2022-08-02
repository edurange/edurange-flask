import "./reading.styles.css"
class Reading extends React.Component {
    render() {
        // TODO get readings in the json contents file rather than reading the files from the front end
        // fetch(`./readings/${this.props.fileName}`).then((resp) => {reading = resp.text()})
        return (
            <div className='edu-reading'>
                <h3>Reading Section Goes Here</h3>
                <p>Render reading from markdown into here.</p>
            </div>
        );
    }
}

export default Reading;