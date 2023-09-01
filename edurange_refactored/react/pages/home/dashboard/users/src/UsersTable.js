
import React, {useContext} from 'react';
import { MainFrameContext } from '../../../main_frame/MainFrame';

import '../main/NewDash.css'
import '../main/tables.css'

function UsersTable() {
    const { session_instructorData_state } = useContext(MainFrameContext);
    const tempData = session_instructorData_state.users || [];  

    return (
        <div className="newdash-datatable-frame">
            <div className="newdash-datatable-header">
                <div className='table-cell-item table-user-id' >ID</div>
                <div className='table-cell-item table-username' >Username</div>
                <div className='table-cell-item table-email'>Email</div>
                <div className='table-cell-item table-created'>Created At</div>
                <div className='table-cell-item table-role'>Role</div>
                <div className='table-cell-item table-active' >Active</div>
            </div>
            {tempData.slice(1).map((user, index) => (
                <div key={index} className="table-row">
                    <div className='table-cell-item table-user-id'>{user.id}</div>
                    <div className='table-cell-item table-username'>{user.username}</div>
                    <div className='table-cell-item table-email'>{user.email}</div>
                    <div className='table-cell-item table-created'>{user.created_at}</div>
                    <div className='table-cell-item table-role'>{user.role}</div>
                    <div className='table-cell-item table-active'>{user.is_active ? "true":"false"}</div>
                    
                    
                </div>
            ))}
        </div>
    );
}

export default UsersTable;

