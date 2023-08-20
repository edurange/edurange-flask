import React from 'react';
import UsersTable from './UsersTable';
import '../main/NewDash.css'
function Users () {
    return (
        <div>
            <div className='newdash-content-placard'>Students</div>
            <UsersTable/>
        </div>
    );
}

export default Users;