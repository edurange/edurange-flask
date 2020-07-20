"""Helper utilities and decorators."""
from flask import flash, abort, request, session, redirect, url_for
from flask_login import current_user
from flask_table import Table, Col
from jwt.jwk import jwk_from_dict, OctetJWK

from . import tasks
from .user.models import User, Scenarios, StudentGroups, GroupUsers
from .user.models import generate_registration_code as grc
from edurange_refactored.user.forms import GroupForm, addUsersForm, manageInstructorForm, modScenarioForm, deleteStudentForm
from edurange_refactored.extensions import db

import json
import os

path_to_key = os.path.dirname(os.path.abspath(__file__))


def load_key_data(name, mode='rb'):
    abspath = os.path.normpath(os.path.join(path_to_key, 'templates/utils/.keys', name))
    with open(abspath, mode=mode) as fh:
        return fh.read()


class TokenHelper:

    def __init__(self):
        self.data = jwk_from_dict(json.loads(load_key_data('oct.json', 'r')))
        self.octet_obj = OctetJWK(self.data.key, self.data.kid)

    def get_JWK(self):
        return self.octet_obj

    def get_data(self):
        return self.data

    def verify(self, token):
        self.octet_obj.verify()


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)

class CheckCol(Col):
    def td_format(self, content):
        return '<div class="form-check">\n\t<input type="checkbox" class="form-check-input" value="">\n</div>'


# Old code for tables on the dashboards (possibly not used anymore? [tbd])------

class StudentTable(Table):
    classes = ['table']
    thead_classes = ['thead-dark']
    state = CheckCol('')
    id = Col('id')
    username = Col('username')
    email = Col('email')
    html_attrs = {
        'data-toggle': 'table',
        'data-pagination': 'true',
        'data-show-columns': 'true',
        'data-multiple-select-row': 'true',
        'data-click-to-select': 'true',
        'overflow-y': 'scroll'} # html_attrs probably don't do anything


class Student(object):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email


class GroupTable(Table):
    classes = ['table']
    thead_classes = ['thead-dark']
    id = Col('id')
    name = Col('name')
    html_attrs = {
        'data-toggle': 'table',
        'data-search': 'true',
        'data-search-on-enter-key': 'true',
        'data-show-columns': 'true',
        'data-multiple-select-row': 'true',
        'data-click-to-select': 'true',
        'data-pagination': 'true'}


class Group(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class GroupUserTable(Table):
    classes = ['table']
    thead_classes = ['thead-dark']
    id = Col('id')
    username = Col('username')
    email = Col('email')
    html_attrs = {
        'data-toggle': 'table',
        'data-search': 'true',
        'data-search-on-enter-key': 'true',
        'data-show-columns': 'true',
        'data-multiple-select-row': 'true',
        'data-click-to-select': 'true',
        'data-pagination': 'true'}


class GroupUser(object):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email


class UserInfoTable(Table):
    classes = ['table']
    thead_classes = ['thead-dark']
    id = Col('id')
    username = Col('username')
    email = Col('email')


class UserInfo(object):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email


class ScenarioTable(Table):
    classes = ['table']
    thead_classes = ['thead_dark']
    id = Col('id')
    name = Col('name')
    created_at = Col('created_at')
    status = Col('status')


class Scenario(object):
    def __init__(self, id, name, created_at, status):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.status = status

#----------------------------------------------------------

# WARNING:
# This check is actually vulnerable to attacks.
# Since we're retrieving user id from the session request variables, it can be spoofed
# Although it requires knowledge of the admin user_id #, it will often just be '1'
# TODO: Harden check_admin()

def check_admin():
    #number = session.get('user_id')
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if not user.is_admin:
        abort(403)

def check_instructor():
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if not user.is_instructor:
        abort(403)

def check_role_view(mode): # check if view mode compatible with role (admin/inst/student)
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if not user.is_admin and not user.is_instructor:
        abort(403) # student's don't need their role checked
        return None # a student has no applicable role. does abort stop the calling/parent function?
    else:
        mode = request.args['mode']
        if mode not in ['studentView', 'instructorView', 'adminView']:
            abort(400) # only supported views
        elif user.is_instructor and not user.is_admin: # instructor only
            if mode == 'studentView':
                return True # return true since viewMode should be set
            elif mode == 'adminView':
                abort(403) # instructors can't choose adminView
            else:
                return False # return false since viewMode should be dropped
        elif user.is_admin:
            if mode in ['studentView', 'instructorView']:
                return True
            else:
                return False
        else:
            abort(403) # who are you?!
            return None


def process_request(form):  # Input must be request.form  # WIP
    dataKeys = []
    for k in form.keys():
        dataKeys.append(k)

    form_switch = {
        "modScenarioForm":         ["csrf_token", "sid", "mod_scenario"],
        "startScenario":            ["csrf_token", "start_scenario", "stop_scenario"],
        "GroupForm":                ["csrf_token", "name", "create"],
        "deleteStudentForm":        ["csrf_token", "stuName", "delete_student"],
        "manageInstructorForm":     ["csrf_token", "uName", "promote"],
        # "unmakeInstructorForm": ["csrf_token", "iName", "unmake_instructor"],
        "addUsersForm":             ["csrf_token", "add", "groups", "uids"]
    }

    switchVals = []
    for v in form_switch.values():
        switchVals.append(v)
    switchKeys = []
    for k in form_switch.keys():
        switchKeys.append(k)

    i = 0
    for l in switchVals:
        if l == dataKeys:
            i = switchVals.index(l)
    f = switchKeys[i]
    # print(f)

    process_switch = {
        "modScenarioForm":         process_scenarioModder,
        "startScenario":            process_scenarioStarter,
        "GroupForm":                process_groupMaker,
        "deleteStudentForm":        process_delStu,
        "manageInstructorForm":     process_manInst,
        # "unmakeInstructorForm": process_instDest(),
        "addUsersForm":             process_addUser
    }
    return process_switch[f]()



def process_scenarioModder():  # Form submitted to create a scenario |  # makeScenarioForm
    sM = modScenarioForm(request.form)
    if sM.validate_on_submit():
        sid = sM.sid.data
        action = sM.mod_scenario.data

        return {"Start": tasks.start,
                "Stop" : tasks.stop,
                "Destroy" : tasks.destroy
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
        StudentGroups.create(name=name, owner_id=session.get('_user_id'), code=code)
        flash('Created group {0}'.format(name))

        #return redirect(url_for('dashboard.admin'))


def process_manInst():  # Form to give a specified user instructor permissions |  # manageInstructorForm
    mI = manageInstructorForm(request.form)
    if request.form.get('promote') == "true":
        if mI.validate_on_submit():
            uName = mI.uName.data
            user = User.query.filter_by(username=uName).first()
            user.update(is_instructor=True)

            flash('Made {0} an Instructor.'.format(uName))
            #return redirect(url_for('dashboard.admin'))
        else:
            flash_errors(mI)
        #return redirect(url_for('dashboard.admin'))

    elif request.form.get('promote') == "false":
        if mI.validate_on_submit():
            uName = mI.uName.data
            user = User.query.filter_by(username=uName).first()
            user.update(is_instructor=False)

            flash('Demoted {0} from Instructor status.'.format(uName))
            #return redirect(url_for('dashboard.admin'))
        else:
            flash_errors(mI)
        #return redirect(url_for('dashboard.admin'))


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
        #return redirect(url_for('dashboard.admin'))
    else:
        flash_errors(uD)
    #return redirect(url_for('dashboard.admin'))


def process_addUser():  # Form to add or remove selected students from a selected group |  # addUsersForm
    uA = addUsersForm(request.form)
    if request.form.get('add') == "true":
        if uA.validate_on_submit():
            db_ses = db.session

            if len(uA.groups.data) < 1:
                flash('A group must be selected')
                return

            group = uA.groups.data

            gid = db_ses.query(StudentGroups.id).filter(StudentGroups.name == group).first()[0]
            uids = uA.uids.data  # string form
            if uids[-1] == ',':
                uids = uids[:-1]  # slice last comma to avoid empty string after string split
            uids = uids.split(',')
            for i, uid in reversed(list(enumerate(uids))):
                check = db_ses.query(GroupUsers).filter(GroupUsers.user_id == uid, GroupUsers.group_id == gid).first()
                if check is not None:
                    flash('User already in group.', 'error')
                    uids.pop(i)
                    pass
                else:
                    GroupUsers.create(user_id=uid, group_id=gid)
            flash('Added {0} users to group {1}. DEBUG: {2}'.format(len(uids), group, uids))
            return True # this was an ajax request
        else:
            flash_errors(uA)
            return True

    elif request.form.get('add') == "false":
        if uA.validate_on_submit():
            db_ses = db.session

            if len(uA.groups.data) < 1:
                flash('A group must be selected')
                return

            group = uA.groups.data

            gid = db_ses.query(StudentGroups.id).filter(StudentGroups.name == group).first()[0]
            uids = uA.uids.data  # string form
            if uids[-1] == ',':
                uids = uids[:-1]  # slice last comma to avoid empty string after string split

            uids = uids.split(',')

            for i, uid in reversed(list(enumerate(uids))):
                check = db_ses.query(GroupUsers).filter(GroupUsers.user_id == uid, GroupUsers.group_id == gid).first()
                if check is not None:  # if user is in group
                    check.delete()
                else:
                    flash('User ID {0} not in group.'.format(uid), 'error')
                    uids.pop(i)

            flash('Removed {0} users from group {1}. DEBUG: {2}'.format(len(uids), group, uids))
            return True # this was an ajax request
        else:
            flash_errors(uA)
            return True

#
