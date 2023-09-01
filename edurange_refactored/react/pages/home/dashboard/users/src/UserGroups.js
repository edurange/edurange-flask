import React from 'react';

import '../main/NewDash.css'
import UserGroupsTable from './UserGroupsTable';

function UserGroups () {
    return (
        <div>
            <div className='newdash-content-placard'>
                Student Groups
            </div>
            <UserGroupsTable/>
        </div>
    );
}

export default UserGroups;