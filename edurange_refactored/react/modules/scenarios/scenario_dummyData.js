
// use GuideQuestion_Shell
export const fakeAnswers = [
    {
        question_text : "something",
        question_isEssay : false,
        answer_expected : "something1",
        answer_isCorrect : false,
        answer_history : ["something","something","something","something","something","something","something"],
        score_current : 0,
        score_max : 3,
    },
    {
        question_text : "second",
        question_isEssay : false,
        answer_expected : "second2",
        answer_isCorrect : false,
        answer_history : ["second","second","second","second","second","second","second"],
        score_current : 0,
        score_max : 3,
    },
    {
        question_text : "third",
        question_isEssay : false,
        answer_expected : "third3",
        answer_isCorrect : false,
        answer_history : ["third","third","third","third","third","third","third"],
        score_current : 0,
        score_max : 3,
    },
]

// // use GuidePage_shell
// const fakePages = [
//     {
//         uid : 1234,
//         pageNumber : 1,
//         q_and_a : fakeAnswers,
//     },
//     {
//         uid : 2345,
//         pageNumber : 2,
//         q_and_a : fakeAnswers,
//     },
//     {
//         uid : 3456,
//         pageNumber : 3,
//         q_and_a : fakeAnswers,
//     },
// ]

// // use ScenarioGuide_shell
// const fakeScenarios = [

//     {
//         dbid : 1234,
//         uid : 9876,
//         title : "something",
//         active : true,
//         pages : fakePages,
//     },
//     {
//         dbid : 2345,
//         uid : 8765,
//         title : "something2",
//         active : true,
//         pages : fakePages,
//     },
//     {
//         dbid : 3456,
//         uid : 7654,
//         title : "something3",
//         active : true,
//         pages : fakePages,
//     },
// ]

// // use UserScenarioCatalog_shell
// const fakeCatalog = [
//     {
//         uid : 1234,
//         scenarios : fakeScenarios
//     },
// ]

// function buildScenarioGuide (input) {

//     return 0;
// }