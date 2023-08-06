import React, { useState } from 'react';

function ChangeEmailForm() {

    // State to hold form values - initialize with blank form state
    const [formData, setFormData] = useState({ name: '', email: '', });


    // user changes fields -> update state
    function handleInputChange(event) {
        const { name, value } = event.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    }

    // Handle form submission (you can implement this according to your needs)
    const handleSubmit = (event) => {

        event.preventDefault(); // this diverts default html form submission behavior to allow for JS logic

        // Insert your logic to handle form submission here...
        // For demonstration purposes, we're just logging the form data
        console.log(formData);

    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="name">Name:</label>
                <input
                    className="form-control"
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    placeholder="Enter your name"
                />
            </div>

            <div className="form-group">
                <label htmlFor="email">Email:</label>
                <input
                    className="form-control"
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="Enter your email"
                />
            </div>

            <button type="submit" name="update" value="email" class="btn btn-dark">Submit</button>
        </form>
    );
};

export default ChangeEmailForm;