
import React, {useContext} from 'react';
import { MainFrameContext } from '../../MainFrame';
//HOOKS//////////////////////////////////////

  // hook declarations:

  // imported props:
  
  /////////////////////////////////////////////
  import './UsersTable_temp.css';

function ScenariosTable_temp() {
    const { session_instructorData_state } = useContext(MainFrameContext);
    const tempData = session_instructorData_state.scenarios || [];  

    return (
        <div className="users-table">
            <div className="table-header">
                <div>created_at</div>
                <div>description</div>
                <div>ID</div>
                <div>Name</div>
                <div>Owner ID</div>
                <div>Is Active</div>
                <div>scenarioGroups_memberOf</div>
                <div>userGroup_members</div>
            </div>
            {tempData.map((scneario, index) => (
                <div key={index} className="table-row">
                    <div>{scneario.created_at}</div>
                    <div>{scneario.description}</div>
                    <div>{scneario.id}</div>
                    <div>{scneario.name}</div>
                    <div>{scneario.ownerID}</div>
                    <div>{scneario.status ? 1 : 0}</div>
                    <div>{scneario.scenarioGroups_memberOf}</div>
                    <div>{scneario.studentGroup_members}</div>
                </div>
            ))}
        </div>
    );
}

export default ScenariosTable_temp;
//   function ScenarioGroupsTable_temp() {
//     const { instructorData_state } = useContext(MainFrameContext);
//     const tempData = instructorData_state.users || [];  

//     return (
//         <div className="users-table">
//             <div className="table-header">
//                 <div>Group Name</div>
//                 <div>Created At</div>
//                 <div>Scenario ID</div>
//                 <div>OWner ID</div>
//                 <div>Status</div>
//                 <div>User Groups</div>
//             </div>
//             {tempData.map((userGroup, index) => (
//                 <div key={index} className="table-row">
//                     <div>{userGroup.username}</div>
//                     <div>{userGroup.email}</div>
//                     <div>{userGroup.created_at}</div>
//                     <div>{userGroup.id}</div>
//                     <div>{userGroup.role}</div>
//                     <div>{userGroup.is_active ? "true":"false"}</div>
//                     <div>{userGroup.userGroups_memberOf}</div>
//                     <div>{userGroup.scenarios_memberOf}</div>
//                 </div>
//             ))}
//         </div>
//     );
// }

// export default ScenariosTable_temp;
