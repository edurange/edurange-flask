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
                {/* <h1>Reading Section Goes Here</h1>
                <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.</p>
                <p>Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. <mark id='code'>Console.WriteLine("Hello World");</mark> Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus.</p>
                <h2>Reading Section Goes Here</h2>
                <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.</p>
                <h3>Reading Section Goes Here</h3>
                <p>Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. <mark id='code'>Console.WriteLine("Hello World");</mark> Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus.</p> */}
            </div>
        );
    }
}

export default Reading;