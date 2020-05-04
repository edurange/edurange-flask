# -*- coding: utf-8 -*-
"""User views."""
from flask import abort, Blueprint, flash, redirect, render_template, request, url_for, session
from flask_login import login_required, current_user
from flask_table import BoolCol
from edurange_refactored.user.forms import EmailForm, GroupForm, GroupFinderForm, addUsersForm
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
    return render_template("dashboard/student.html", infoTable=infoTable)

@blueprint.route("/instructor", methods=['GET'])
@login_required
def instructor():
    check_instructor()
    curId = session.get('_user_id')
    db_ses = db.session
    groups = db_ses.query(StudentGroups.id.label('gid'), StudentGroups.name, User.id.label('uid'), User.username, GroupUsers).filter(StudentGroups.owner_id == curId).filter(StudentGroups.id == GroupUsers.group_id).filter(GroupUsers.user_id == User.id)
    userInfo = db_ses.query(User.id, User.username, User.email).filter(User.id == curId)
    infoTable = UserInfoTable(userInfo)
    if request.method == 'GET':
        return render_template('dashboard/instructor.html', groups=groups, infoTable=infoTable)

@blueprint.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    check_admin()
    students = User.query.all()
    stuTable = StudentTable(students)
    groups = StudentGroups.query.all()
    groTable = GroupTable(groups)
    groupNames = []
    scenarios = Scenarios.query.all()
    scenarioTable = ScenarioTable(scenarios)
    for g in groups:
        groupNames.append(g.name)
    if request.method == 'GET':
        form = EmailForm()
        form1 = GroupForm()
        form2 = GroupFinderForm()
        return render_template('dashboard/admin.html', groTable=groTable, form=form, form1=form1, form2=form2, groups=groupNames, students=students)
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
        return redirect(url_for('user.admin'))
    elif request.form.get('groups') is not None:
        form = addUsersForm(request.form)
        if form.validate_on_submit():
            db_ses = db.session
            group = form.groups.data
            gid = db_ses.query(StudentGroups.id).filter(StudentGroups.name == group).limit(1)

            uids = form.uid.data

            for uid in uids:
                check = db_ses.query(GroupUsers.id).filter(GroupUsers.user_id == uid).limit(1)
                if any(check):
                    flash('User already in group.')
                    pass
                else:
                    GroupUsers.create(user_id=uid, group_id=gid)
                    flash('Added {0} users to group {1}. DEBUG: {2}'.format(len(uids), group, uids))


            return redirect(url_for('dashboard.admin'))
        else:
            flash_errors(form)
        return redirect(url_for('dashboard.admin'))
#TODO: add function for adding users to groups

    # elif request.form.get('user_group') is not None:
    #     form = addUsersForm(request.form)
    #     if form.validate_on_submit():
    #         group = form.user_group.data
    #
    #         # TODO: make add group users functional
    #         # for user in user_list
    #         #   add user to group
