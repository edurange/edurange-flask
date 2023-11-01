
import { nanoid } from 'nanoid';
import React from 'react';
import { edurange_icons } from '../../ui/edurangeIcons';


export async function fetchScenarioList() {
    try {
        const response = await axios.get("/api/get_scenarios");
        if (response.data.scenarioTable) {
            return response.data.scenarioTable;
        };
    }
    catch (error) { console.log('get_scenarios_list error:', error); };
};


export async function getScenarioMeta(scenario_id) {
    try {
        const response = await axios.get("/api/get_scenario_meta");
        if (response.data.meta) {
            return response.data.meta;
        };
    }
    catch (error) { console.log('get_scenarios_meta error:', error); };
};

