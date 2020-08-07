import os

from flask import current_app, flash, request, session
from flask_login import current_user

from edurange_refactored.extensions import db
from edurange_refactored.user.forms import (
    GroupForm,
    addUsersForm,
    deleteStudentForm,
    manageInstructorForm,
    modScenarioForm,
    scenarioResponseForm
)

from . import tasks
from .user.models import GroupUsers, StudentGroups, User, Responses
from .user.models import generate_registration_code as grc
from .utils import flash_errors, responseCheck


def process_request(form):  # Input must be request.form
    dataKeys = []
    for k in form.keys():
        dataKeys.append(k)

    form_switch = {
        "modScenarioForm":          ["csrf_token", "sid", "mod_scenario"],
        "startScenario":            ["csrf_token", "start_scenario", "stop_scenario"],
        "GroupForm":                ["csrf_token", "name", "create", "size"],
        "deleteStudentForm":        ["csrf_token", "stuName", "delete_student"],
        "manageInstructorForm":     ["csrf_token", "uName", "promote"],
        "addUsersForm":             ["csrf_token", "add", "groups", "uids"],
        "scenarioResponseForm":     ["csrf_token", "response", "scenario", "question"]
    }

    switchVals = []
    for v in form_switch.values():
        switchVals.append(v)
    switchKeys = []
    for k in form_switch.keys():
        switchKeys.append(k)

    i = 0
    for li in switchVals:
        if li == dataKeys:
            i = switchVals.index(li)
    f = switchKeys[i]
    # print(f)

    process_switch = {
        "modScenarioForm":          process_scenarioModder,
        "startScenario":            process_scenarioStarter,
        "GroupForm":                process_groupMaker,
        "deleteStudentForm":        process_delStu,
        "manageInstructorForm":    process_manInst,
        "addUsersForm":             process_addUser,
        "scenarioResponseForm":     process_scenarioResponse
    }
    return process_switch[f]()


def process_scenarioModder():  # Form submitted to create a scenario |  # makeScenarioForm
    sM = modScenarioForm(request.form)  # type2Form(request.form)  #
    if sM.validate_on_submit():
        sid = sM.sid.data  # string1.data  #
        action = sM.mod_scenario.data  # string2.data  #

        return {"Start": tasks.start, "Stop": tasks.stop, "Destroy": tasks.destroy}[
            action
        ].delay(sid)


def process_scenarioStarter():  # Form submitted to start or stop an existing scenario
    if request.form.get("start_scenario") is not None:
        os.chdir("/home/xennos/Desktop/edurange-flask/data/tmp/Foo")
        os.system("terraform apply -auto-approve")

    elif request.form.get("stop_scenario") is not None:
        os.chdir("/home/xennos/Desktop/edurange-flask/data/tmp/Foo")
        os.system("terraform destroy -auto-approve")


def process_groupMaker():  # Form to create a new group |  # GroupForm
    gM = GroupForm(request.form)  # type1Form(request.form)  #
    if gM.validate_on_submit():
        code = grc()
        name = gM.name.data
        group = StudentGroups.create(name=name, owner_id=session.get('_user_id'), code=code)
        users = []
        size = gM.size.data
        if size == 0:
            flash('Created group {0}'.format(name), 'success')
            return 'utils/create_group_response.html', group, users
        else:
            pairs = []
            gid = group.get_id()
            fName = name # formatted group name
            name = name.replace(" ", "") # group name with no spaces
            j = 0
            for i in range(1, size + 1):
                username = "{0}-user{1}".format(name, i)
                password = grc()
                user = User.create(
                    username=username,
                    email=username+"@edurange.org".format(i),
                    password=password,
                    active=True,
                    is_static=True
                )
                uid = user.get_id()
                GroupUsers.create(user_id=uid, group_id=gid)
                j += 1
                pairs.append((username, password))
                users.append(user)
            flash('Created group {0} and populated it with {1} accounts'.format(fName, j), 'success')
            return 'utils/create_group_response.html', group, users, pairs
    else:
        flash_errors(gM)
        return 'utils/create_group_response.html',



def process_manInst():  # Form to give a specified user instructor permissions |  # manageInstructorForm
    mI = manageInstructorForm(request.form)
    if request.form.get("promote") == "true":
        if mI.validate_on_submit():
            uName = mI.uName.data  # string1.data  #
            user = User.query.filter_by(username=uName).first()
            user.update(is_instructor=True)

            flash("Made {0} an Instructor.".format(uName))
        else:
            flash_errors(mI)

    elif request.form.get("promote") == "false":
        if mI.validate_on_submit():
            uName = mI.uName.data  # string1.data  #
            user = User.query.filter_by(username=uName).first()
            user.update(is_instructor=False)

            flash("Demoted {0} from Instructor status.".format(uName))
        else:
            flash_errors(mI)


def process_delStu():  # WIP Form to delete a specified student from the database |  # deleteStudentForm
    db_ses = db.session
    uD = deleteStudentForm(request.form)  # type1Form(request.form)  #
    if uD.validate_on_submit():
        stuName = uD.stuName.data  # string1.data  #
        user = User.query.filter_by(username=stuName).first()
        stuId = db_ses.query(User.id).filter(User.username == stuName)
        gu = db_ses.query(GroupUsers).filter(GroupUsers.user_id == stuId)
        gu.delete()
        user.delete()

        flash("User {0} has been deleted.".format(stuName))
    else:
        flash_errors(uD)


def process_addUser():  # Form to add or remove selected students from a selected group |  # addUsersForm
    uA = addUsersForm(request.form)

    if uA.validate_on_submit():
        db_ses = db.session
        group = uA.groups.data
        gid = db_ses.query(StudentGroups.id).filter(StudentGroups.name == group).first()[0]
        group = db_ses.query(StudentGroups).filter(StudentGroups.id == gid).first()
        uids = uA.uids.data  # string form
        adding = False

        if uids[-1] == ",":
            uids = uids[
                :-1
            ]  # slice last comma to avoid empty string after string split
        uids = uids.split(",")

        if request.form.get("add") == "true":
            adding = True

        for i, uid in reversed(list(enumerate(uids))):
            check = (
                db_ses.query(GroupUsers)
                .filter(GroupUsers.user_id == uid, GroupUsers.group_id == gid)
                .first()
            )
            if check is not None:
                if adding:
                    uids.pop(i)
                else:
                    check.delete()
            else:
                if adding:
                    GroupUsers.create(user_id=uid, group_id=gid)
                else:
                    uids.pop(i)

        if adding:
            flash(
                "Added {0} users to group {1}. DEBUG: {2}".format(
                    len(uids), group.name, uids
                ),
                "success",
            )
        else:
            flash('Removed {0} users from group {1}. DEBUG: {2}'.format(len(uids), group.name, uids), 'success')
        users = db_ses.query(User.id, User.username, User.email).filter(StudentGroups.id == gid, StudentGroups.id == GroupUsers.group_id, GroupUsers.user_id == User.id)
        return 'utils/manage_student_response.html', group, users
    else:
        flash_errors(uA)


def process_scenarioResponse():
    sR = scenarioResponseForm()
    if sR.validate_on_submit():
        sid = sR.scenario.data
        qnum = sR.question.data
        resp = sR.response.data
        uid = current_user.id
        # answer checking function in utils
        gotIt = responseCheck(resp)
        # get attempt number from somewhere
        att = 0
        Responses.create(user_id=uid, scenario_id=sid, question=qnum, student_response=resp, correct=gotIt, attempt=att)


