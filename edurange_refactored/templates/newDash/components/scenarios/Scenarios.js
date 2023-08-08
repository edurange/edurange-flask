import React from 'react';
import ScenariosTable from './ScenariosTable';
import '../main/NewDash.css'
function Scenarios () {
    return (
        <div>
            <div className='newdash-content-placard' >Scenarios</div>
            <ScenariosTable/>
        </div>
    );
}

export default Scenarios;
