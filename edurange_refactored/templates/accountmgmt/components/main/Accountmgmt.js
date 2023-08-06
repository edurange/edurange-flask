import "./Accountmgmt.css";
import {createRoot} from 'react-dom/client';
import React, { useState, useEffect } from 'react';
import ChangeEmailForm from "../email-form/ChangeEmailForm";

// main component
function Accountmgmt(props) {

//HOOKS//////////////////////////////////////

  // hook declarations:

  // imported props:
  const {
    activeTab_state,  update_tabChoice_status,
    login_state,      update_login_status,
    csrfToken_state,  update_csrfToken_status,
    connectIP, connectPort, loginRoute, userInfo_state


//     user={e.attributes.user.value}
//     username={e.attributes.username.value}
//     created_at={e.attributes.created_at.value}
//     is_admin={e.attributes.is_admin.value}
//     is_instructor={e.attributes.is_instructor.value}

  } = useContext(MainFrameContext);

/////////////////////////////////////////////

    
    
    // helper functions (in scope of Accountmgmt)
    function parseUserType (input) {
        if (userInfo_state.role === "Administrator") {return <h2 className="mb-0 ml-auto pr-1">Admin</h2>;}
        else if (userInfo_state.role === "Instructor") {return <h2 className="mb-0 ml-auto pr-1">Instructor</h2>;}
        else  {return <h2 className="mb-0 ml-auto pr-1">Student</h2>;};
    };
    // function parseGroupLabel(input) {
    //     if (props.label === "Temp. Member Of") {return <dd className="col-sm-8"> {input.groupCount} </dd>;}
    //     else {return <dd className="col-sm-8"> {input.groupCount} groups</dd>;}
    // }

    // const tempLabel = parseGroupLabel(props);   
    const tempUserType = parseUserType(props);

return (
    <div>
        <div className="container mt-2 mb-2">
            <h1>Account Management</h1>
        </div>
        <div className="container">
            <div className="card mb-2 mt-2">
                <div className="card-header">
                    <div className="row">
                        <div className="ml-3 mb-0">
                            <h3> <i className="fa-solid fa-user"></i> Account Information </h3>
                        </div>
                        {tempUserType}
                    </div>
                </div>
            <div className="card-body">
                <div className="row mb-3 mx-2">
                    <div className="col-sm-6">
                        <dl className="row mb-0">
                            <dt className="col-sm-3"> Name </dt>
                            <dd className="col-sm-9"> {userInfo_state.username} </dd>
                        </dl>
                        <dl className="row mb-0">
                            <dt className="col-sm-3"> Email </dt>
                            <dd className="col-sm-9"> {userInfo_state.email} </dd>
                        </dl>
                    </div>
                    <div className="col-sm-6">
                        {/* <dl className="row mb-0"> */}
                            {/* <dt className="col-sm-4"> {userInfo_state.label} </dt> */}
                            {/* {tempLabel} */}
                        {/* </dl> */}
                        <dl className="row mb-0">
                            <dt className="col-sm-4"> Created At </dt>
                            <dd className="col-sm-8"> {userInfo_state.created_at} </dd>
                        </dl>
                    </div>
                </div>
            </div>
        </div>
    <div className="row">
        <div className="col-sm-6 mt-2">
            <div className="card bg-light mb-3">
                <div className="card-header">Change Email</div>
                <div className="card-body">
                    <h5 className="card-text"></h5>
                    <ChangeEmailForm/>
                </div>
            </div>
        </div>
    </div>
</div>
</div>
       );
};
export default Accountmgmt;

// var e = document.getElementById("acct-mgmt-id");
// const root=createRoot(e);


// root.render(<Accountmgmt 
//     user_email={e.attributes.user_email.value}
//     emailForm={e.attributes.emailForm.value}
//     groupCount={e.attributes.groupCount.value}
//     label={e.attributes.label.value}
//     user={e.attributes.user.value}
//     username={e.attributes.username.value}
//     created_at={e.attributes.created_at.value}
//     is_admin={e.attributes.is_admin.value}
//     is_instructor={e.attributes.is_instructor.value}
// />);

