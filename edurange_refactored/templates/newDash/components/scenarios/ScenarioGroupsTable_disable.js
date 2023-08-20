
import React, {useContext} from 'react';
import { MainFrameContext } from '../../../main_frame/MainFrame'
import '../main/NewDash.css'

//HOOKS//////////////////////////////////////

  // hook declarations:

  // imported props:
  
  /////////////////////////////////////////////
  
  function ScenarioGroupsTable() {
    
    const { session_instructorData_state } = useContext(MainFrameContext);

    const tempData = session_instructorData_state.userGroups || [];  // assign to extant array OR empty (avoids undefined error)

    return (
        <table>
            <thead>            
                <tr>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Created At</th>
                    <th>ID</th>
                    <th>Role</th>
                    <th>Is Active</th>
                </tr>
            </thead>
            <tbody>
                {tempData.map((userGroup, index) => (
                <tr key={index}>
                    <td>{userGroup.code}</td>
                    <td>{userGroup.is_hidden}</td>
                    <td>{userGroup.id}</td>
                    <td>{userGroup.name}</td>
                    <td>{userGroup.ownerID}</td>
                    <td>{userGroup.student_members}</td>
                    <td>{userGroup.scenarios_member_of}</td>
                </tr>
                ))}
            </tbody>
        </table>
    );
}

export default ScenarioGroupsTable;
