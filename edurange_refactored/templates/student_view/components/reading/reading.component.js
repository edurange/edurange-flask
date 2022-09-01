import React from 'react';
import "./reading.styles.css"

class Reading extends React.Component {
    createMarkup() {
        return {__html: this.props.reading};
    }
    eduReading() {
        return <div dangerouslySetInnerHTML={this.createMarkup()} />;
    }
    render() {
        // TODO get readings in the json contents file rather than reading the files from the front end
        // fetch(`./readings/${this.props.fileName}`).then((resp) => {reading = resp.text()})
        return (
            <div className='edu-reading' id='edu-reading'>
                {this.eduReading()}
            </div>
        );
    }
}

export default Reading;