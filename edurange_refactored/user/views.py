# -*- coding: utf-8 -*-
"""User views."""
from flask import abort, Blueprint, flash, redirect, render_template, request, url_for, session
from flask_login import login_required, current_user
from flask_table import BoolCol
from edurange_refactored.user.forms import EmailForm, GroupForm, GroupFinderForm, addUsersForm, makeInstructorForm, unmakeInstructorForm, deleteStudentForm
from .models import User, StudentGroups, GroupUsers, Scenarios
from .models import generate_registration_code as grc
from ..utils import StudentTable, Student, GroupTable, Group, GroupUserTable, GroupUser, flash_errors, ScenarioTable, UserInfoTable
from edurange_refactored.tasks import send_async_email
from edurange_refactored.extensions import db

blueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard", static_folder="../static")

# WARNING:
# This check is actually vulnerable to attacks.
# Since we're retrieving user id from the session request variables, it can be spoofed
# Although it requires knowledge of the admin user_id #, it will often just be '1'
# TODO: Harden check_admin()

def check_admin():
    #number = session.get('_user_id')
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if not user.is_admin:
        abort(403)

def check_instructor():
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if not user.is_instructor:
        abort(403)

@blueprint.route("/")
@login_required
def student():
    """List members."""
    db_ses = db.session
    curId = session.get('_user_id')
    userInfo = db_ses.query(User.id, User.username, User.email).filter(User.id == curId)
    infoTable = UserInfoTable(userInfo)
    memberOf = db_ses.query(StudentGroups.id, StudentGroups.name, GroupUsers).filter(GroupUsers.user_id == curId).filter(GroupUsers.group_id == StudentGroups.id)
    return render_template("dashboard/student.html", infoTable=infoTable, memberOf=memberOf)

@blueprint.route("/scenarios")
@login_required
def scenarios():
    """List scenarios.s"""""
    check_admin()
    scenarios = Scenarios.query.all()
    # scenarioTable = ScenarioTable(scenarios)

    return render_template("dashboard/scenarios.html", scenarios=scenarios)

@blueprint.route("/instructor", methods=['GET', 'POST'])
@login_required
def instructor():
    check_instructor()
    curId = session.get('_user_id')
    db_ses = db.session
    #groups = db_ses.query(StudentGroups.id.label('gid'), StudentGroups.name, StudentGroups.code, User.id.label('uid'), User.username, GroupUsers).filter(StudentGroups.owner_id == curId).filter(StudentGroups.id == GroupUsers.group_id).filter(GroupUsers.user_id == User.id)
    groups = db_ses.query(StudentGroups.id, StudentGroups.name, StudentGroups.code).filter(StudentGroups.owner_id == curId)
    userInfo = db_ses.query(User.id, User.username, User.email).filter(User.id == curId)
    infoTable = UserInfoTable(userInfo)
    if request.method == 'GET':
        form = GroupForm()
        return render_template('dashboard/instructor.html', form=form, groups=groups, infoTable=infoTable)

    elif request.form.get('name') is not None:
        form = GroupForm(request.form)
        if form.validate_on_submit():
            code = grc()
            name = form.name.data
            StudentGroups.create(name=name, owner_id=session.get('_user_id'), code=code)
            flash('Created group {0}'.format(name))
            return redirect(url_for('dashboard.instructor'))

@blueprint.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    check_admin()
    db_ses = db.session
    students = db_ses.query(User.id, User.username, User.email).filter(User.is_instructor == False)
    instructors = db_ses.query(User.id, User.username, User.email).filter(User.is_instructor == True)
    stuTable = StudentTable(students)
    groups = StudentGroups.query.all()
    groTable = GroupTable(groups)
    groupNames = []
    db_ses = db.session
    users_per_group = {}

    for g in groups:
        groupNames.append(g.name)

    for name in groupNames:
        users_per_group[name] = []
        groupUsers = db_ses.query(User.id, User.username, User.email, StudentGroups, GroupUsers).filter(StudentGroups.name == name).filter(StudentGroups.id == GroupUsers.group_id).filter(GroupUsers.user_id == User.id)
        users_per_group[name].append(groupUsers)

    if request.method == 'GET':
        form = EmailForm()
        form1 = GroupForm()
        form2 = GroupFinderForm()

        return render_template('dashboard/admin.html', stuTable=stuTable, groTable=groTable, form=form, form1=form1, form2=form2, groups=groups, students=students, instructors=instructors, usersPGroup=users_per_group)

    elif request.form.get('to') is not None:
        form = EmailForm(request.form)
        if form.validate_on_submit():
            email_data = {
                'subject' : form.subject.data,
                'to': form.to.data,
                            'body': form.body.data
            }
            email = form.to.data
            if request.form['submit'] == 'Send':
                send_async_email.delay(email_data)
                flash('Sending email to {0}'.format(email))
            else:
                send_async_email.apply_async(args=[email_data], countdown=60)
                flash('An email will be sent to {0} in one minute.'.format(email))
            return redirect(url_for('dashboard.admin'))

    elif request.form.get('name') is not None:
        form = GroupForm(request.form)
        if form.validate_on_submit():
            code = grc()
            name = form.name.data
            StudentGroups.create(name=name, owner_id = session.get('_user_id'), code=code)
            flash('Created group {0}'.format(name))

            return redirect(url_for('dashboard.admin'))

    elif request.form.get('group') is not None:
        form = GroupFinderForm(request.form)
        if form.validate_on_submit():
            db_ses = db.session
            name = form.group.data
            groupUsers = db_ses.query(User.id, User.username, User.email, StudentGroups, GroupUsers).filter(StudentGroups.name == name).filter(StudentGroups.id == GroupUsers.group_id).filter(GroupUsers.user_id == User.id)
            groUTable = GroupUserTable(groupUsers)
            return render_template('dashboard/admin.html', students=students, groTable=groTable, groUTable=groUTable, form=form, groups=groupNames)
        else:
            flash_errors(form)
        return redirect(url_for('dashboard.admin'))

    #elif request.form.get('groups') is not None:
    elif request.form.get('add') is not None:
        form = addUsersForm(request.form)
        if form.validate_on_submit():
            db_ses = db.session

            if len(form.groups.data) < 1:
                flash('A group must be selected')
                return redirect(url_for('dashboard.admin'))

            group = form.groups.data

            gid = db_ses.query(StudentGroups.id).filter(StudentGroups.name == group)
            uids = form.uids.data # string form
            if uids[-1] == ',':
                uids = uids[:-1] # slice last comma to avoid empty string after string split
            uids = uids.split(',')
            for i,uid in enumerate(uids):
                check = db_ses.query(GroupUsers.id).filter(GroupUsers.user_id == uid)
                if any(check):
                    flash('User already in group.', 'error')
                    uids.pop(i-1)
                    pass
                else:
                    GroupUsers.create(user_id=uid, group_id=gid)


            flash('Added {0} users to group {1}. DEBUG: {2}'.format(len(uids), group, uids))
            return redirect(url_for('dashboard.admin'))
        else:
            flash_errors(form)
        return redirect(url_for('dashboard.admin'))

    elif request.form.get('uName') is not None:
        form = makeInstructorForm(request.form)
        if form.validate_on_submit():
            uName = form.uName.data
            user = User.query.filter_by(username=uName).first()
            user.update(is_instructor=True)

            flash('Made {0} an Instructor.'.format(uName))
            return redirect(url_for('dashboard.admin'))
        else:
            flash_errors(form)
        return redirect(url_for('dashboard.admin'))

    elif request.form.get('iName') is not None:
        form = unmakeInstructorForm(request.form)
        if form.validate_on_submit():
            iName = form.iName.data
            user = User.query.filter_by(username=iName).first()
            user.update(is_instructor=False)

            flash('Demoted {0} from Instructor status.'.format(iName))
            return redirect(url_for('dashboard.admin'))
        else:
            flash_errors(form)
        return redirect(url_for('dashboard.admin'))

    elif request.form.get('stuName') is not None:
        form = deleteStudentForm(request.form)
        if form.validate_on_submit():
            stuName = form.stuName.data
            user = User.query.filter_by(username=stuName).first()
            stuId = db_ses.query(User.id).filter(User.username == stuName)
            gu = db_ses.query(GroupUsers).filter(GroupUsers.user_id == stuId)
            gu.delete()
            user.delete()

            flash('User {0} has been deleted.'.format(stuName))
            return redirect(url_for('dashboard.admin'))
        else:
            flash_errors(form)
        return redirect(url_for('dashboard.admin'))

    elif request.form.get('remove') is not None:
        form = addUsersForm(request.form)
        if form.validate_on_submit():
            db_ses = db.session
            group = form.groups.data

            gid = db_ses.query(StudentGroups.id).filter(StudentGroups.name == group)
            uids = form.uids.data # string form
            if uids[-1] == ',':
                uids = uids[:-1] # slice last comma to avoid empty string after string split

            miss = 0 # count user ids that are not in group
            uids = uids.split(',')

            for i, uid in enumerate(uids):
                user = db_ses.query(GroupUsers).filter(GroupUsers.user_id == uid and GroupUsers.id == gid).first()
                if user is not None: # if user is in group
                    user.delete()
                else:
                    miss += 1

            flash('Removed {0} users from group {1}.'.format(len(uids) - miss, group))
            return redirect(url_for('dashboard.admin'))
        else:
            flash_errors(form)
        return redirect(url_for('dashboard.admin'))
