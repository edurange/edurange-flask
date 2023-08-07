
import React, {useContext} from 'react';
import { MainFrameContext } from '../../../main_frame/MainFrame';

import './UsersTable_temp.css';

function UsersTable_temp() {
    const { session_instructorData_state } = useContext(MainFrameContext);
    const tempData = session_instructorData_state.users || [];  

    return (
        <div className="users-table">
            <div className="table-header">
                <div>Username</div>
                <div>Email</div>
                <div>Created At</div>
                <div>ID</div>
                <div>Role</div>
                <div>Is Active</div>
                <div>User Groups</div>
                <div>Scenarios</div>
            </div>
            {tempData.map((user, index) => (
                <div key={index} className="table-row">
                    <div>{user.username}</div>
                    <div>{user.email}</div>
                    <div>{user.created_at}</div>
                    <div>{user.id}</div>
                    <div>{user.role}</div>
                    <div>{user.is_active ? "true":"false"}</div>
                    <div>{user.userGroups_memberOf}</div>
                    <div>{user.scenarios_memberOf}</div>
                </div>
            ))}
        </div>
    );
}

export default UsersTable_temp;
