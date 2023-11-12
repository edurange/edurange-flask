
// not currently in use and may need updates; keep

import { nanoid } from "nanoid";

function assignUserRole(inputData) {
    if (inputData.is_admin) { return 'Administrator' }
    else if (inputData.is_instructor) { return 'Instructor' }
    else { return 'Student' }
};

const formatDate = (inputDate) => {
    const dateToprocess = new Date(inputDate) ?? new Date('Dec 25, -0001');
    const month = String(dateToprocess.getMonth() + 1).padStart(2, '0'); // Months are 0-based
    const day = String(dateToprocess.getDate()).padStart(2, '0');
    const year = String(dateToprocess.getFullYear()).slice(-2); // Get the last 2 characters of the year
    const hours = String(dateToprocess.getHours()).padStart(2, '0');
    const minutes = String(dateToprocess.getMinutes()).padStart(2, '0');
    
    return `${month}/${day}/${year} ${hours}:${minutes}`;
};

export class UserShell {
    constructor(input = {}) {
        this.id = input.id ?? 'none';
        this.uid = nanoid(5);
        this.username = input.username ?? 'none';
        this.role = (input.username) ? assignUserRole(input) : 'none'; // assigns role if user exists, otherwise 'none'
        this.is_active = input.active || false;
        this.email = input.email ?? 'none';
        this.userGroups_memberOf = input.userGroups_memberOf ?? [];
        this.scenarios_memberOf = input.scenarios_memberOf ?? [];
        this.created_at = formatDate (input.created_at) ?? 'none';
    };
};
export class UserGroupShell {
    constructor(input = {}) {
        this.code = input.code ?? 'none';
        this.id = input.id ?? 'none';
        this.is_hidden = input.is_hidden || true;
        this.name = input.name ?? "none";
        this.ownerID = input.owner_id ?? "none";
        this.user_members = input.user_members ?? [];
        this.scenarios_memberOf = input.scenario_memberOf ?? [];
    };
};
export class ScenarioShell {
    constructor(input = {}) {
        this.id = input.scenario_id ?? 'none';
        this.uid = nanoid(5);
        this.name = input.scenario_name ?? 'none';
        this.description = input.scenario_description ?? 'none';
        this.ownerID = input.scenario_owner_id ?? 'none';
        this.status = input.scenario_status ?? 'none';
        this.studentGroup_members = input.studentGroup_members ?? [];
        this.scenarioGroups_memberOf = input.scenarioGroups_memberOf ?? [];
        this.created_at = formatDate(input.scenario_created_at) ?? 'none';
    };
};
export class ScenarioGroupShell {
    constructor(input = {}) {
        this.id = input.scenario_group_id ?? "none";
        this.studentGroup_members = input.studentGroup_members ?? [];
    };
};