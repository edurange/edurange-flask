# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, redirect, render_template, request, url_for, session, flash, current_app
from flask_login import login_required
from edurange_refactored.user.forms import GroupForm, addUsersForm, manageInstructorForm, modScenarioForm, \
    deleteStudentForm, makeScenarioForm
from .models import User, StudentGroups, GroupUsers, Scenarios, ScenarioUsers
from ..tasks import CreateScenarioTask
from ..utils import UserInfoTable, check_admin, check_instructor, process_request, flash_errors
from ..scenario_utils import populate_catalog
from edurange_refactored.extensions import db
import os

blueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard", static_folder="../static")


@blueprint.route("/")
@login_required
def student():
    """List members."""
    # Queries for the user dashboard
    db_ses = db.session
    curId = session.get('_user_id')

    userInfo = db_ses.query(User.id, User.username, User.email).filter(User.id == curId)
    infoTable = UserInfoTable(userInfo)

    memberOf = db_ses.query(StudentGroups.id, StudentGroups.name, GroupUsers).filter(GroupUsers.user_id == curId).filter(GroupUsers.group_id == StudentGroups.id)

    scenarioTable = db_ses.query(Scenarios.name.label('sname'), Scenarios.description.label('type'), StudentGroups.name.label('gname'), User.username.label('iname')).filter(GroupUsers.user_id == curId).filter(StudentGroups.id == GroupUsers.group_id).filter(ScenarioUsers.user_id == GroupUsers.user_id).filter(Scenarios.owner_id == User.id)

    return render_template("dashboard/student.html", infoTable=infoTable, memberOf=memberOf, scenarioTable=scenarioTable)

@blueprint.route("/catalog", methods=['GET'])
@login_required
def catalog():
    check_admin()
    scenarios = populate_catalog()
    groups = StudentGroups.query.all()
    form = modScenarioForm(request.form)

    return render_template("dashboard/catalog.html", scenarios=scenarios, groups=groups, form=form)

@blueprint.route("/make_scenario", methods=['POST'])
@login_required
def make_scenario():
    check_admin()
    form = makeScenarioForm(request.form)
    if form.validate_on_submit():
        db_ses = db.session
        name = request.form.get('scenario_name')
        infoFile = './scenarios/prod/' + name + '/' + name + '.yml'
        owner = session.get('_user_id')
        group = request.form.get('scenario_group')
        students = db_ses.query(User.username).filter(StudentGroups.name == group).filter(StudentGroups.id == GroupUsers.group_id).filter(GroupUsers.user_id == User.id).all()
        print(students)
        print(students)
        CreateScenarioTask.delay(name, infoFile, owner, students)
        flash("Success, your scenario will appear shortly. This page will automatically update. Students Found: {}".format(students), "success")
    else:
        flash_errors(form)

    return redirect(url_for('dashboard.scenarios'))



@blueprint.route("/scenarios", methods=['GET', 'POST'])
@login_required
def scenarios():
    """List of scenarios and scenario controls"""
    check_admin()
    scenarioModder = modScenarioForm()
    scenarios = Scenarios.query.all()
    groups = StudentGroups.query.all()

    if request.method == 'GET':
        return render_template("dashboard/scenarios.html", scenarios=scenarios, scenarioModder=scenarioModder, groups=groups)

    elif request.method == 'POST':
        process_request(request.form)
        return render_template("dashboard/scenarios.html", scenarios=scenarios, scenarioModder=scenarioModder, groups=groups)


@blueprint.route("/instructor", methods=['GET', 'POST'])
@login_required
def instructor():
    """List of an instructors groups"""
    check_instructor()
    # Queries for the owned groups table
    curId = session.get('_user_id')
    db_ses = db.session
    groups = db_ses.query(StudentGroups.id, StudentGroups.name, StudentGroups.code).filter(StudentGroups.owner_id == curId)
    userInfo = db_ses.query(User.id, User.username, User.email).filter(User.id == curId)
    infoTable = UserInfoTable(userInfo)
    if request.method == 'GET':
        groupMaker = GroupForm()
        return render_template('dashboard/instructor.html', groupMaker=groupMaker, groups=groups, infoTable=infoTable)

    elif request.method == 'POST':
        process_request(request.form)
        return redirect(url_for('dashboard.admin'))


@blueprint.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    """List of all students and groups. Group, student, and instructor management forms"""
    check_admin()
    db_ses = db.session
    # Queries for the tables of students and groups
    students = db_ses.query(User.id, User.username, User.email).filter(User.is_instructor == False)
    instructors = db_ses.query(User.id, User.username, User.email).filter(User.is_instructor == True)
    groups = StudentGroups.query.all()
    groupNames = []
    users_per_group = {}

    for g in groups:
        groupNames.append(g.name)

    for name in groupNames:
        users_per_group[name] = []
        groupUsers = db_ses.query(User.id, User.username, User.email, StudentGroups, GroupUsers).filter(StudentGroups.name == name).filter(StudentGroups.id == GroupUsers.group_id).filter(GroupUsers.user_id == User.id)
        users_per_group[name].append(groupUsers)

    if request.method == 'GET':
        groupMaker = GroupForm()
        userAdder = addUsersForm()
        instructorManager = manageInstructorForm()
        userDropper = deleteStudentForm()

        return render_template('dashboard/admin.html', groupMaker=groupMaker, userAdder=userAdder, instructorManager=instructorManager, userDropper=userDropper, groups=groups, students=students, instructors=instructors, usersPGroup=users_per_group)

    elif request.method == 'POST':
        process_request(request.form)
        return redirect(url_for('dashboard.admin'))

