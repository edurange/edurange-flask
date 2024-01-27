import axios from 'axios';
import React, { useEffect, useContext, useState } from 'react';

import '../../scenarios/src/list/ScenarioTable.css';

function Instructor_ScenDetail({scenario_detail}) {

    console.log(scenario_detail)
    return (
        <div>
            <div>
                SCENARIO DETAILS TOP BAR
            </div>
            <div>
                SCENARIO DETAILS MAIN SPACE
                <div>
                    MAIN SPACE COLUMN LABEL ROW
                    <div>
                    scenario_created_at {scenario_detail.scenario_created_at}
                    </div>
                    <div>
                    scenario_description {scenario_detail.scenario_description}
                    </div>
                    <div>
                    scenario_id {scenario_detail.scenario_id}
                    </div>
                    <div>
                    scenario_name {scenario_detail.scenario_name}
                    </div>
                    <div>
                    scenario_owner_id {scenario_detail.scenario_owner_id}
                    </div>
                    <div>
                    scenario_status {scenario_detail.scenario_status}
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Instructor_ScenDetail;