// place any jQuery/helper plugins in here, instead of separate, slower script files.
//

function addUser(uid) {
	let sel = document.forms['addGroupUsers']['selection'].value;
	var chk = sel.includes(uid);
	if (chk == true) {
	//	document.forms['addGroupUsers']['selection'].value = sel.replace('{{student.id}},', '')
		document.forms['addGroupUsers']['selection'].value = sel.replace(uid + ',', '');
	} else {
		//document.forms['addGroupUsers']['selection'].value += '{{student.id}},'
		document.forms['addGroupUsers']['selection'].value += uid + ',';
	}
}

