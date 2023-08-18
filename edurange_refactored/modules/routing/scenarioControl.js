



// main functionality for the scenario user guide view / questions.


function getScenarioQuestions( userID, scenarioInstanceID ) {

    

}
function getUserScenarioData( userID, scenarioInstanceID ) {

    const userScenarioData = {

        currentScenarioInstances : [],


    }

}


const neededUserScenarioData =  {

    scenario_DBID: 4,               // to identify the specific scenario from the DataBase (use actual DBID, not nanoid gen'd)
    scenario_userIsActive : true,       // maybe unneeded. we wouldn't be looking here if it weren't the case

    scenario_question_status: [

        [
            [5, 5],  // points for each question and a bool for whether it was answered correctly
            [0, 5], // could use another representation, maybe a tuple or dict
            [5, 5]   // but array allows for easier dynamic distribution and the order will never change, so it makes sense and easy enough to make sense of and remember
        ],
        [
            [0, 4],  
            [0, 2], 
            [0, 5]  
        ]


    ],

    scenario_session_responses: [
        "cat ls",
        "man ls",
        "ls -l"
    ],

    scenario_response_archive: "some_database_reference",


}