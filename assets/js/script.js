// App initialization code goes here
export function check_user_list(number) {
  const students = document.forms.addGroupUsers.selection.value;
  students.append('0');
  let i;
  for (i = 0; i !== students.length; i++) {
    if (students[i] === number) {
      break;
    } else document.forms.addGroupUsers.selection.value += number;
  }
}
