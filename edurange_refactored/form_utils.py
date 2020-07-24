from flask import request, flash, session, current_app

from . import tasks
from .user.models import User, StudentGroups, GroupUsers
from .user.models import generate_registration_code as grc
from .utils import flash_errors
from edurange_refactored.user.forms import GroupForm, addUsersForm, manageInstructorForm, modScenarioForm, \
    deleteStudentForm
from edurange_refactored.extensions import db

import os


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
        "modScenarioForm":         process_scenarioModder,
        "startScenario":            process_scenarioStarter,
        "GroupForm":                process_groupMaker,
        "deleteStudentForm":        process_delStu,
        "manageInstructorForm":     process_manInst,
        "addUsersForm":             process_addUser,
        "removeUsersForm":          process_addUser
    }
    return process_switch[f]()


def process_scenarioModder():  # Form submitted to create a scenario |  # makeScenarioForm
    sM = modScenarioForm(request.form)
    if sM.validate_on_submit():
        sid = sM.sid.data
        action = sM.mod_scenario.data

        return {"Start": tasks.start,
                "Stop": tasks.stop,
                "Destroy": tasks.destroy
                }[action].delay(sid)


def process_scenarioStarter():  # Form submitted to start or stop an existing scenario
    if request.form.get('start_scenario') is not None:
        os.chdir('/home/xennos/Desktop/edurange-flask/data/tmp/Foo')
        os.system('terraform apply -auto-approve')

    elif request.form.get('stop_scenario') is not None:
        os.chdir('/home/xennos/Desktop/edurange-flask/data/tmp/Foo')
        os.system('terraform destroy -auto-approve')


def process_groupMaker():  # Form to create a new group |  # GroupForm
    gM = GroupForm(request.form)
    if gM.validate_on_submit():
        code = grc()
        name = gM.name.data
        gid = (StudentGroups.create(name=name, owner_id=session.get('_user_id'), code=code)).get_id()
        size = gM.size.data
        if size == 0:
            flash('Created group {0}'.format(name))
        else:
            fName = name # formatted group name
            name = name.replace(" ", "") # group name with no spaces
            j = 0
            for i in range(1, size + 1):
                username = "{0}-user{1}".format(name, i)
                password = grc()
                uid = (User.create(
                    username=username,
                    email=username+"@edurange.org".format(i),
                    password=password,
                    active=True,
                )).get_id()
                GroupUsers.create(user_id=uid, group_id=gid)
                j += 1
                current_app.logger.info("User made: {0} | Password: {1}".format(username, password))
            flash('Created group {0} and populated it with {1} accounts'.format(fName, j))



def process_manInst():  # Form to give a specified user instructor permissions |  # manageInstructorForm
    mI = manageInstructorForm(request.form)
    if request.form.get('promote') == 'true':
        if mI.validate_on_submit():
            uName = mI.uName.data
            user = User.query.filter_by(username=uName).first()
            user.update(is_instructor=True)

            flash('Made {0} an Instructor.'.format(uName))
        else:
            flash_errors(mI)

    elif request.form.get('promote') == 'false':
        if mI.validate_on_submit():
            uName = mI.uName.data
            user = User.query.filter_by(username=uName).first()
            user.update(is_instructor=False)

            flash('Demoted {0} from Instructor status.'.format(uName))
        else:
            flash_errors(mI)


def process_delStu():  # WIP Form to delete a specified student from the database |  # deleteStudentForm
    db_ses = db.session
    uD = deleteStudentForm(request.form)
    if uD.validate_on_submit():
        stuName = uD.stuName.data
        user = User.query.filter_by(username=stuName).first()
        stuId = db_ses.query(User.id).filter(User.username == stuName)
        gu = db_ses.query(GroupUsers).filter(GroupUsers.user_id == stuId)
        gu.delete()
        user.delete()

        flash('User {0} has been deleted.'.format(stuName))
    else:
        flash_errors(uD)


def process_addUser():  # Form to add or remove selected students from a selected group |  # addUsersForm
    uA = addUsersForm(request.form)

    if uA.validate_on_submit():
        db_ses = db.session
        group = uA.groups.data
        gid = db_ses.query(StudentGroups.id).filter(StudentGroups.name == group).first()[0]
        uids = uA.uids.data  # string form
        adding = False

        if uids[-1] == ',':
            uids = uids[:-1]  # slice last comma to avoid empty string after string split
        uids = uids.split(',')

        if request.form.get('add') == 'true':
            adding = True

        for i, uid in reversed(list(enumerate(uids))):
            check = db_ses.query(GroupUsers).filter(GroupUsers.user_id == uid, GroupUsers.group_id == gid).first()
            if check is not None:
                if adding:
                    # flash('User already in group.', 'warning')
                    uids.pop(i)
                else:
                    check.delete()
            else:
                if adding:
                    GroupUsers.create(user_id=uid, group_id=gid)
                else:
                    # flash('User {0} not in group.'.format(uid), 'warning')
                    uids.pop(i)

        if adding:
            flash('Added {0} users to group {1}. DEBUG: {2}'.format(len(uids), group, uids), 'success')
        else:
            flash('Removed {0} users from group {1}. DEBUG: {2}'.format(len(uids), group, uids), 'success')

    else:
        flash_errors(uA)
