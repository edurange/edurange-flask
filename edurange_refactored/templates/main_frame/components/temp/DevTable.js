
import React, {useContext} from 'react';
import { MainFrameContext } from '../../MainFrame';
import MainFrame from '../../MainFrame'

import UserGroupsTable_temp from './../../../newDash/components/users/UserGroupsTable_temp';
import UsersTable_temp from './../../../newDash/components/users/UsersTable_temp';
import ScenariosTable_temp from './../../../newDash/components/scenarios/ScenariosTable_temp';
import ScenarioGroupsTable_temp from './../../../newDash/components/scenarios/ScenarioGroupsTable_temp';

import '../../../newDash/components/users/UsersTable_temp.css'

function DevTable() {
    const { session_instructorData_state } = useContext(MainFrameContext);
    const tempData = session_instructorData_state.scenarios || [];  

    return (
                <div className='temp-divvy'>
                    {/* <UsersTable_temp/>
                    USERS
                    <UserGroupsTable_temp/>
                    GROUPS
                    <ScenariosTable_temp/>
                    SCENARIOS
                    <ScenarioGroupsTable_temp/>
                    SCENARIO GROUPS */}
                </div>
    );
};
export default DevTable;