
import React, {useContext} from 'react';
import { Link } from 'react-router-dom';

import '../../../../src/Dashboard.css'
import '../../../../src/tables.css'
import { HomeRouterContext } from '../../../../../src/Home_router';

function ScenariosListView() {
    
    
    const { instructorData_state } = useContext(HomeRouterContext);
    if (!instructorData_state.scenarios) {return (<>No Scenarios Available</>)}

    console.log('scenario list view reporting instructordatastate:',instructorData_state)
    
    const tempData = (instructorData_state.scenarios.length > 0) ? instructorData_state.scenarios : [];  

    if (tempData.length < 1) {return (<>No Scenarios Available</>)}

    return (
        <>
        <div className='newdash-content-placard' >Scenarios</div>
            
        <div className="newdash-datatable-frame">
            <div className="newdash-datatable-header">
                <div className='table-cell-item table-active' >UID</div>
                <div className='table-cell-item table-scenario-name'>Title</div>
                <div className='table-cell-item table-active' >Owner</div>
                <div className='table-cell-item table-active' >Status</div>
                <div className='table-cell-item table-created'>Created</div>
            </div>
            {tempData.slice(1).map((scenario) => (
                <Link key={scenario.id} to ={`${scenario.uid}/home`}>
                    <div className="table-row">
                        <div className='table-cell-item table-active'>{scenario.uid}</div>
                        <div className='table-cell-item table-scenario-name'>{scenario.name}</div>
                        <div className='table-cell-item table-active'>{scenario.ownerID}</div>
                        <div className='table-cell-item table-active'>{scenario.status ? "true":"false"}</div>
                        <div className='table-cell-item table-created'>{scenario.created_at}</div>
                    </div>
                </Link>
            ))}
        </div>
    </>
    );
}

export default ScenariosListView;