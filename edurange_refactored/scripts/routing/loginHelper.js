// import React from 'react'
import { nanoid } from 'nanoid'

// the 'recombobulate' process will take the data from the backend, as available, and repopulate it into a more dev-friendly and
// useful structure for the frontend, consisting of object arrays.

// all of these classes are going in arrays where their ID aligns with their array index.
// this is particularly important for the User class, where the ID is considered a sensitive piece of information 
// that should NOT be exposed to visitors.  admins will have a way to get this information elsewhere if needed
// therefore the 'id' field will be overwritten with a unique identifier rather than the database's actual user ID.

// however, as mentioned, the index of the users in the sessionData.instructor.users array that they will belong to will 
// align 1:1 with their actual database ID, because a 'dummy' data item will be placed at the 0th index of each array
// before the real items are pushed on top.

// that of course means that, when using these arrays, start at index 1 and not 0, unless you want to display the dummy
// data for some reason.

// all of this data is only stored in browser/js memory for the session, and its availability will depend on the user's
// role as defined by the backend.  in other words, admin data will not be ever be sent to a non-admin's browser to begin with,
// so no amt of simple browser tampering will provide any extra information.

// ?? operator will assign 'none' if value is nullish (undefined, null) but otherwise preserves falsy values like 0


const formatDate = (inputDate) => {
    const dateToprocess = new Date(inputDate) ?? new Date('Dec 25, -0001');
    const month = String(dateToprocess.getMonth() + 1).padStart(2, '0'); // Months are 0-based
    const day = String(dateToprocess.getDate()).padStart(2, '0');
    const year = String(dateToprocess.getFullYear()).slice(-2); // Get the last 2 characters of the year
    const hours = String(dateToprocess.getHours()).padStart(2, '0');
    const minutes = String(dateToprocess.getMinutes()).padStart(2, '0');
    
    return `${month}/${day}/${year} ${hours}:${minutes}`;
};


class UserShell {
    constructor(input = {}) {
        this.id = input.id ?? 'none';
        this.username = input.username ?? 'none';
        this.role = (input.username) ? assignUserRole(input) : 'none'; // assigns role if user exists, otherwise 'none'
        this.is_active = input.active || false;
        this.email = input.email ?? 'none';
        // this.id = input.id ? nanoid(8) : 'none'; // assigns unique (sessionlong) id if user exists, otherwise 'none'
        this.userGroups_memberOf = input.userGroups_memberOf ?? [];
        this.scenarios_memberOf = input.scenarios_memberOf ?? [];
        this.created_at = formatDate(input.created_at) ?? 'none';
    };
};
class UserGroupShell {
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
class ScenarioShell {
    constructor(input = {}) {
        this.id = input.scenario_id ?? 'none';
        this.name = input.scenario_name ?? 'none';
        this.description = input.scenario_description ?? 'none';
        this.ownerID = input.scenario_owner_id ?? 'none';
        this.status = input.scenario_status ?? 'none';
        this.studentGroup_members = input.studentGroup_members ?? [];
        this.scenarioGroups_memberOf = input.scenarioGroups_memberOf ?? [];
        this.created_at = formatDate(input.scenario_created_at) ?? 'none';
    };
};
class ScenarioGroupShell {
    constructor(input = {}) {
        this.id = input.scenario_group_id ?? "none";
        this.studentGroup_members = input.studentGroup_members ?? [];
    };
};
export function assignUserRole(inputData) {
    if (inputData.is_admin) { return 'Administrator' }
    else if (inputData.is_instructor) { return 'Instructor' }
    else { return 'Student' }
};

export function makeFirstPass(inputObj) {

    function processUsers(inputData) {
        const inputUserArray = inputData.instructor_data[0];
        const tempUserArray = [];
        tempUserArray.push(new UserShell());
        if (inputUserArray) {
            inputUserArray.forEach(user => {
                const currentUser = new UserShell(user)
                tempUserArray.push(currentUser);
            });
        };

        return tempUserArray;
    };
    function processUserGroups(inputData) {

        const outputArray = [];
        outputArray.push(new UserGroupShell());

        inputData.forEach((group) => {
            const tempGroup = new UserGroupShell(group);
            outputArray.push(new UserGroupShell(group));
        });

        return outputArray;
    }

    function processScenarios(inputData) {
        const inputScenarioArray = inputData.instructor_data[3];
        const tempScenarioArray = [];
        tempScenarioArray.push(new ScenarioShell());
        if (inputScenarioArray) {
            inputScenarioArray.forEach(scenario => {
                const currentScenario = new ScenarioShell(scenario)
                tempScenarioArray.push(currentScenario);
            });
        };
        return tempScenarioArray;
    };
    function processScenarioGroups(inputData) {
        const inputScenarioGroupArray = inputData.instructor_data[4];
        const tempScenarioGroupArray = [];
        tempScenarioGroupArray.push(new ScenarioGroupShell());
        if (inputScenarioGroupArray) {
            inputScenarioGroupArray.forEach((scenarioGroup) => {
                const currentScenarioGroup = new ScenarioGroupShell(scenarioGroup)
                tempScenarioGroupArray.push(currentScenarioGroup);
            });
        };
        return tempScenarioGroupArray;
    };

    const processedUsers = processUsers(inputObj);
    const processedUserGroups = processUserGroups(inputObj.instructor_data[1]);
    const processedScenarios = processScenarios(inputObj);
    const processedScenarioGroups = processScenarioGroups(inputObj);

    const firstPassOutput = {
        users: processedUsers,
        userGroups: processedUserGroups,
        scenarios: processedScenarios,
        scenarioGroups: processedScenarioGroups
    };

    return firstPassOutput;
};

function assignGroupsToUsers(firstPassObj, originalObj) {

    const users = originalObj[0];
    const userGroupAssignments = originalObj.instructor_data[2];

    const outputObj = { ...firstPassObj };

    for (let user of outputObj.users) {
        user.userGroups_memberOf = [];
    };

    for (let assignment of userGroupAssignments) {
        const userId = assignment.user_id;
        const groupId = assignment.group_id;

        if (outputObj.users[userId]) {
            outputObj.users[userId].userGroups_memberOf.push(groupId);
        } else { console.warn(`User with id ${userId} not found.`); 
        };
    };

    return outputObj;
};

function assignUsersToGroups(firstPassObj, originalObj) {
    const outputObj = { ...firstPassObj };
    const userGroupAssignments = originalObj.instructor_data[2];

    for (let assignment of userGroupAssignments) {
        const userId = assignment.user_id;
        const groupId = assignment.group_id;

        if (outputObj.userGroups[groupId]) {
            if (!outputObj.userGroups[groupId].user_members.includes(userId)) {
                outputObj.userGroups[groupId].user_members.push(userId); 
            }
        } else { console.warn(`Group with id ${groupId} not found.`); 
        };
    };

    return outputObj;
}

function assignScenariosToGroups(newObject, inputObj) {
    const scenarioGroupAssignments = inputObj.instructor_data[4];

    const outputObj = { ...newObject };

    for (let assignment of scenarioGroupAssignments) {
        const studentGroupId = assignment.student_group_id;
        const scenarioGroupId = assignment.scenario_group_id;

        if (outputObj.userGroups[studentGroupId]) {
            outputObj.userGroups[studentGroupId].scenarios_memberOf.push(scenarioGroupId);
        } else { console.warn(`UserGroup with id ${studentGroupId} not found.`); 
        }

        if (outputObj.scenarioGroups[scenarioGroupId]) {
            outputObj.scenarioGroups[scenarioGroupId].studentGroup_members.push(studentGroupId)
        } else { console.warn(`ScenarioGroup with id ${scenarioGroupId} not found.`); 
        };
    };
    return outputObj;
};

export function makeSecondPass(firstPassObj, originalObj) {

    const groupsAssignedToUsersObj = assignGroupsToUsers(firstPassObj, originalObj);
    const usersAssignedtoGroupsObj = assignUsersToGroups(groupsAssignedToUsersObj, originalObj);
    const scenariosAssignedToGroups = assignScenariosToGroups(usersAssignedtoGroupsObj, originalObj);

    return scenariosAssignedToGroups;

};


export function recombobulate(inputObj) {

    if (inputObj) {
        const firstPassOutput = makeFirstPass(inputObj);
        const secondPassOutput = makeSecondPass(firstPassOutput, inputObj);
        return secondPassOutput;
    }
}

export function convertToDivs(result) {
    let output = '';

    function processItem(item) {
        if (typeof item === 'object') {
            if (Array.isArray(item)) { item.forEach(subItem => processItem(subItem)); } 
            else { for (const [key, value] of Object.entries(item)) { processItem(value); }
            }
        } else { output += `<div>${item}</div>\n`;
        }
    }

    processItem(result);

    return (
        <div>
            {output}
        </div>
    );
};