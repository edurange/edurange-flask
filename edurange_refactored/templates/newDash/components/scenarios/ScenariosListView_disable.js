
import React, {useContext} from 'react';
import { MainFrameContext } from '../../../main_frame/MainFrame';
import { Link } from 'react-router-dom';

import ScenarioFullView from './ScenarioFullView';
import ScenarioCardDetail from './ScenarioCardDetail';

import '../main/NewDash.css'
import '../main/tables.css'

function ScenariosListView() {
    const { session_instructorData_state } = useContext(MainFrameContext);
    const tempData = session_instructorData_state.scenarios || [];  

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