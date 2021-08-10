/* 
This script catches the interrupt signal made by pressing ctrl+c in order to perform cleanup tasks (such as destroying terraform instances)
*/

var exec = require("child_process").exec;

// while (true) {
//     SingleEntryPlugin.
//     process.on('SIGINT', function () {
//         console.log("exit keystroke caught");
//         // process.exit();
//         // exec("pwd",
//         //     function (error, stdout, stderr) {
//         //         console.log(stdout);
//         //     }
//         // );
//     });
// }