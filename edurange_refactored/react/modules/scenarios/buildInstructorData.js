
// import React from 'react'
import { nanoid } from 'nanoid'

import { UserShell, UserGroupShell, ScenarioGroupShell, ScenarioShell } from '../shells/instructorData_shells';

// the 'buildInstructorDAta' process will take the data from the backend, as available, and repopulate it into a more dev-friendly and
// useful structure for the frontend, consisting of object arrays.

// all of these classes are going in arrays where their ID aligns with their array index.
// this is particularly important for the User class, where the ID is considered a sensitive piece of information 
// that should not be exposed to users.  instead, any time you want to display to a user a scenario's ID or
// a user ID, display the UID, which is a randomly assigned unique ID.

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

function assignUserRole(inputData) {
    if (inputData.is_admin) { return 'Administrator' }
    else if (inputData.is_instructor) { return 'Instructor' }
    else { return 'Student' }
};

function makeFirstPass(inputObj) {

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

function makeSecondPass(firstPassObj, originalObj) {

    const groupsAssignedToUsersObj = assignGroupsToUsers(firstPassObj, originalObj);
    const usersAssignedtoGroupsObj = assignUsersToGroups(groupsAssignedToUsersObj, originalObj);
    const scenariosAssignedToGroups = assignScenariosToGroups(usersAssignedtoGroupsObj, originalObj);

    return scenariosAssignedToGroups;

};


export function buildInstructorData(inputObj) {

    if (inputObj) {
        const firstPassOutput = makeFirstPass(inputObj);
        const secondPassOutput = makeSecondPass(firstPassOutput, inputObj);
        return secondPassOutput;
    }
}

function buildUserData (inputData) {
    return inputData;
}

function convertToDivs(result) {
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