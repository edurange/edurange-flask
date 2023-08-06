
import React, {useContext} from 'react';
import { MainFrameContext } from '../../MainFrame';
// //HOOKS//////////////////////////////////////

//   // hook declarations:

//   // imported props:
  
//   /////////////////////////////////////////////
  
//   function UsersTable_temp() {
    
//     const { instructorData_state } = useContext(MainFrameContext);

//     const tempData = instructorData_state.users || [];  // assign to extant array OR empty (avoids undefined error)

//     return (
//         <table>
//             <thead>            
//                 <tr>
//                     <th>Username</th>
//                     <th>Email</th>
//                     <th>Created At</th>
//                     <th>ID</th>
//                     <th>Role</th>
//                     <th>Is Active</th>
//                     <th>User Groups</th>
//                     <th>Scenarios</th>
//                 </tr>
//             </thead>
//             <tbody>
//                 {tempData.map((user, index) => (
//                 <tr key={index}>
//                     <td>{user.username}</td>
//                     <td>{user.email}</td>
//                     <td>{user.created_at}</td>
//                     <td>{user.id}</td>
//                     <td>{user.role}</td>
//                     <td>{user.is_active ? "true":"false"}</td>
//                     <td>{user.userGroups_memberOf}</td>
//                     <td>{user.scenarios_memberOf}</td>
//                 </tr>
//                 ))}
//             </tbody>
//         </table>
//     );
// }

// export default UsersTable_temp;

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
