
import React, {useContext} from 'react';
import { MainFrameContext } from '../../../main_frame/MainFrame';
import { Link, useParams } from 'react-router-dom';

import '../main/NewDash.css'
import '../main/tables.css'

function ScenariosTable() {
    const { session_instructorData_state } = useContext(MainFrameContext);
    const tempData = session_instructorData_state.scenarios || [];  

    return (
        <div className="newdash-datatable-frame">
            <div className="newdash-datatable-header">
                <div className='table-cell-item table-active' >UID</div>
                <div className='table-cell-item table-scenario-name'>Title</div>
                <div className='table-cell-item table-active' >Owner</div>
                <div className='table-cell-item table-active' >Status</div>
                <div className='table-cell-item table-created'>Created</div>
            </div>
            {tempData.slice(1).map((scenario) => (
                <div key={scenario.uid} className="table-row">
                    <div className='table-cell-item table-active'>{scenario.uid}</div>
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

{/* <div className='newdash-itemcard-image-frame'>
                    <img className='newdash-itemcard-image' src={pointing_finger}/>
                </div>

                <div className="newdash-itemcard-meta-frame">
                    Title: Getting_Started
                </div>

                <div className='newdash-itemcard-meta-row'>
                Students: 2, 3, 4, 5, 6
                </div>

                <div className='newdash-itemcard-meta-row'>
                Difficulty: Easy
                </div>
                        
                <div className='newdash-itemcard-content-frame'>
                    <div className='newdash-itemcard-content-header'></div>
                    <div className='newdash-itemcard-content-main'></div>
                    <div className='newdash-itemcard-content-footer'></div>
                </div> */}