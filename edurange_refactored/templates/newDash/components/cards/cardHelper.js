
import React from "react";

export function buildScenarioTable(inputData){
    
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
        {tempData.map((scenario, index) => (
            <div key={index} className="table-row">
                <div>{scenario.created_at}</div>
                <div>{scenario.description}</div>
                <div>{scenario.id}</div>
                <div>{scenario.name}</div>
                <div>{scenario.ownerID}</div>
                <div>{scenario.status ? 1 : 0}</div>
                <div>{scenario.scenarioGroups_memberOf}</div>
                <div>{scenario.studentGroup_members}</div>
            </div>
        ))}
    </div> 

);

};