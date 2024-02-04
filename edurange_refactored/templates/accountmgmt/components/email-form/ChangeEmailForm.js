import axios from 'axios';
import React, { useState } from 'react';

function ChangeEmailForm() {

    // State to hold form values - initialize with blank form state
    const [formData, setFormData] = useState({ username: '', email: '', });


    // user changes fields -> update state
    function handleInputChange(event) {
        const { name, value } = event.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    }

    // Handle form submission (you can implement this according to your needs)
    async function handleSubmit (event) {

        event.preventDefault(); // this diverts default html form submission behavior to allow for JS logic

        // Insert your logic to handle form submission here...
        // For demonstration purposes, we're just logging the form data
        console.log(formData);
        const username_input = event.target.elements.username.value;
        const newEmail_input = event.target.elements.email.value;
        const email_change_response = await axios.post('/api/change_email', {
            username : username_input,
            email: newEmail_input
        })
        console.log(email_change_response);
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="name">username:</label>
                <input
                    className="form-control"
                    type="text"
                    id="username"
                    name="username"
                    value={formData.username}
                    onChange={handleInputChange}
                    placeholder="Enter your username"
                />
            </div>

            <div className="form-group">
                <label htmlFor="email">email:</label>
                <input
                    className="form-control"
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="Enter new email"
                />
            </div>

            <button type="submit" name="update" value="email" className="btn btn-dark">Submit</button>
        </form>
    );
};

export default ChangeEmailForm;