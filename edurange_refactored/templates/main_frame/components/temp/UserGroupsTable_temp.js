
import React, {useContext} from 'react';
import { MainFrameContext } from '../../MainFrame';

import './UsersTable_temp.css';

function UserGroupsTable_temp() {

  const { session_instructorData_state } = useContext(MainFrameContext);

    const tempData = session_instructorData_state.userGroups || [];  

    return (
        <div className="users-table">
            <div className="table-header">
                <div>Group Code</div>
                <div>Group ID</div>
                <div>is_hidden</div>
                <div>Group Name</div>
                <div>Owner ID</div>
                <div>is_active</div>
                <div>scenarios_memberOf</div>
                <div>user_members</div>
            </div>
            {tempData.map((userGroup, index) => (
                <div key={index} className="table-row">
                    <div>{userGroup.code}</div>
                    <div>{userGroup.id}</div>
                    <div>{userGroup.is_hidden}</div>
                    <div>{userGroup.name}</div>
                    <div>{userGroup.ownerID}</div>
                    <div>{userGroup.is_active ? "true":"false"}</div>
                    <div>{userGroup.scenarios_memberOf}</div>
                    <div>{userGroup.user_members}</div>
                </div>
            ))}
        </div>
    );
}

export default UserGroupsTable_temp;
