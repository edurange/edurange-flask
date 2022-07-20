class Reading extends React.Component {
    render() {
        // TODO get readings in the json contents file rather than reading the files from the front end
        // fetch(`./readings/${this.props.fileName}`).then((resp) => {reading = resp.text()})
        return (
            <div className='guidebox'>
                <h3>Guidebox goes here</h3>
                <p>More guidebox stuff here</p>
            </div>
        );
    }
}

export default Reading;