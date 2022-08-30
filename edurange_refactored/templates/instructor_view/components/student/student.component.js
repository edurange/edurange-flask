import "./student.css"

class Student extends React.Component {
    render() {
        var pg = require('pg');
        var connectionString = "postgres://postgres:passwordfoo@127.0.0.1/ip:5432/namefoo";
        var pgClient = pg.Client(connectionString);
        console.log("Connecting. . .");
        pgClient.connect();
        console.log("Connected!");

        return (
            <div id='student'>Students</div>
        );
    }
}

export default Student;