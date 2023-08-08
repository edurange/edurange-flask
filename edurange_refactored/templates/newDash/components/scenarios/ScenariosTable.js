
import React, {useContext} from 'react';
import { MainFrameContext } from '../../../main_frame/MainFrame';

import '../main/NewDash.css'
import '../main/Tables.css'

function ScenariosTable() {
    const { session_instructorData_state } = useContext(MainFrameContext);
    const tempData = session_instructorData_state.scenarios || [];  

    return (
        <div className="newdash-datatable-frame">
            <div className="newdash-datatable-header">
                <div className='table-cell-item table-user-id' >ID</div>
                <div className='table-cell-item table-scenario-name'>Title</div>
                <div className='table-cell-item table-active' >Owner</div>
                <div className='table-cell-item table-active' >Status</div>
                <div className='table-cell-item table-created'>Created</div>
            </div>
            {tempData.slice(1).map((scenario, index) => (
                <div key={index} className="table-row">
                    <div className='table-cell-item table-user-id'>{scenario.id}</div>
                    <div className='table-cell-item table-scenario-name'>{scenario.name}</div>
                    <div className='table-cell-item table-active'>{scenario.ownerID}</div>
                    <div className='table-cell-item table-active'>{scenario.status ? "true":"false"}</div>
                    <div className='table-cell-item table-created'>{scenario.created_at}</div>
                </div>
            ))}
        </div>
    );
}

export default ScenariosTable;

