
//import button from 'react-bootstrap/Button';

import {createRoot} from 'react-dom/client';
import React, { useState, useEffect } from 'react';
import './student_dashboard.css';


function Student_Dashboard(props) { 
    //hello
    return (
        <div className='dashboard'>
    <div className="container">
            <h1>Welcome {{ current_user, username }}</h1>
            <h3>This is where your scenarios will show up</h3>
        </div><div className="container-narrow" id="accordion">
                <div className="card">
                    <div className="card-header" id="headingInfo">
                        <h5 className="mb-0">
                            <h2> <i className="fa-solid fa-user"></i> User Info </h2>
                            <button className="btn btn-dark" type="button"
                                data-toggle="collapse" data-target="#collapseInfo"
                                aria-expanded="false" aria-controls="collapseInfo">
                                Hide / Show Table
                            </button>
                        </h5>
                    </div>
                    <div id="collapseInfo" className="collapse" aria-labelledby="headingInfo" data-parent="#accordion">
                        <div className="card-body">
                            <div className="col" style="height:100px;">
                                <div>
                                    <table className="table">
                                        <thead className="thead-dark">
                                            <tr>
                                                <th> User ID </th>
                                                <th> Username </th>
                                                <th> Email </th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {userInfo.map(item => (
                                                <tr key={item.id}>
                                                    <td> {item.id} </td>
                                                    <td> {item.username} </td>
                                                    <td> {item.email} </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>

                <div className="card">
                    <div className="card-header" id="headingMemberOf">
                        <h5 className="mb-0">
                            <h2> <i className="fa-solid fa-user"></i> Member Of Groups</h2>
                            <button className="btn btn-dark" type="button" data-toggle="collapse" data-target="#collapseMemberOf" aria-expanded="false" aria-controls="collapseMemberOf">
                                Hide / Show Table
                            </button>
                        </h5>
                    </div>
                    <div id="collapseMemberOf" className="collapse" aria-labelledby="headingMemberOf" data-parent="#accordion">
                        <div className="card-body">

                            <div className="col" style="height:300px;overflow-y:scroll;">
                                <div>
                                    <table className="table">
                                        <thead className="thead-dark">
                                            <tr>
                                                <th> Group ID</th>
                                                <th> Group Name</th>
                                            </tr>
                                        </thead>
                                        <tbody>

                                            <tr>
                                                <td> {group.id}</td>
                                                <td> {group.name}</td>
                                            </tr>

                                        </tbody>
                                    </table>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>

                <div className="card">
                    <div className="card-header" id="headingScenario">
                        <h5 className="mb-0">
                            <h2> <i className="fa-solid fa-code"></i> Scenarios </h2>
                            <button className="btn btn-dark" type="button" data-toggle="collapse" data-target="#collapseScenario" aria-expanded="false" aria-controls="collapseScenario">
                                Hide / Show Table
                            </button>
                        </h5>
                    </div>
                    <div id="collapseScenario" className="collapse" aria-labelledby="headingScenario" data-parent="#accordion">
                        <div className="card-body">

                            <div className="col" style="height:300px;overflow-y:scroll;">
                                <div>
                                    <table className="table">
                                        <thead className="thead-dark">
                                            <tr>
                                                <th> Name </th>
                                                <th> Type </th>
                                                <th> Group </th>
                                                <th> Instructor </th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {/* {% for entry in scenarios %} */<tr>
                                                <td> <a className="btn btn-dark" style="color:White"
                                                    href="{{ '/dashboard/student_scenario/%s'%entry.id }}">
                                                    {entry.sname} </a> </td>
                                                {/* {#} button linking to response page #} */}
                                                <td> {entry.type} </td>
                                                <td> {entry.gname} </td>
                                                <td> {entry.iname} </td>
                                            </tr>}</tbody>
                                    </table>
                                </div>
                            </div>
                            {/* < />!--scenario table stuff--> */}
                        </div>
                    </div>
                </div>
                {/* < />!--scenario table collapse--> */}
               </div> 
               </div> 
               );
}
    var e = document.getElementById('student_dashboard');
    const root=createRoot(e);

    root.render(<Student_Dashboard
        userInfo={e.attributes.userInfo.value}
        groups={e.attributes.groups.value}
        scenarioTable={e.attributes.scenarioTable.value}
    />);   

