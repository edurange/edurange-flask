# -*- coding: utf-8 -*-
"""User views."""
import os
import json
from datetime import datetime

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    send_from_directory,
    url_for,
)
from flask_login import login_required

from edurange_refactored.extensions import db
from edurange_refactored.notification_utils import NotifyCapture
from edurange_refactored.user.forms import (
    GroupForm,
    addUsersForm,
    changeEmailForm,
    deleteGroupForm,
    makeScenarioForm,
    manageInstructorForm,
    modScenarioForm,
    notifyDeleteForm,
    scenarioResponseForm,
)

from ..csv_utils import readCSV, groupCSV
from ..form_utils import process_request
from ..graph_utils import getGraph
from ..role_utils import (
    get_roles,
    scenario_exists,
    student_has_access,
    user_is_admin_and_instructor,
    user_is_admin,
    user_is_instructor
)
from ..scenario_utils import gen_chat_names, identify_state, identify_type, populate_catalog
from ..utils import (
    check_role_view,
    displayCorrectAnswers,
    displayProgress,
    flash_errors,
    getScore,
    responseProcessing,
    getResponses,
    responseSelector,
    tempMaker,
    queryPolish,
    questionReader,
)

from .models import GroupUsers, ScenarioGroups, Scenarios, StudentGroups, User, Responses, Notification


blueprint = Blueprint(
    "dashboard", __name__, url_prefix="/dashboard", static_folder="../static"
)

@blueprint.route("/")
@login_required
def student():
    """List members."""
    # Queries for the user dashboard
    db_ses = db.session
    currentUserId = session.get("_user_id")

    userInfo = db_ses.query(User.id, User.username, User.email).filter(User.id == currentUserId)

    groups = db_ses.query(StudentGroups.id, StudentGroups.name, GroupUsers) \
        .filter(GroupUsers.user_id == currentUserId) \
        .filter(GroupUsers.group_id == StudentGroups.id)

    scenarioTable = (
        db_ses.query(
            Scenarios.id,
            Scenarios.name.label("sname"),
            Scenarios.description.label("type"),
            StudentGroups.name.label("gname"),
            User.username.label("iname"),
        )
        .filter(GroupUsers.user_id == currentUserId)
        .filter(StudentGroups.id == GroupUsers.group_id)
        .filter(User.id == StudentGroups.owner_id)
        .filter(ScenarioGroups.group_id == StudentGroups.id)
        .filter(Scenarios.id == ScenarioGroups.scenario_id)
    )

    return render_template(
        "dashboard/student.html",
        userInfo=userInfo,
        groups=groups,
        scenarioTable=scenarioTable,
    )


@blueprint.route("/account_management", methods=['GET', 'POST'])
@login_required
def account():
    db_ses = db.session
    userId = session.get('_user_id')

    user = db_ses.query(User).filter(User.id == userId).first()

    if user.is_admin or user.is_instructor:
        groupCount = db_ses.query(StudentGroups.id).filter(StudentGroups.owner_id == user.get_id()).count()
        label = "Owner Of"
    elif user.is_static:
        # In this case, groupCount is the name of the group this user is a static member of
        groupCount = db_ses.query(StudentGroups.name) \
            .filter(StudentGroups.id == GroupUsers.group_id, GroupUsers.user_id == user.get_id()) \
            .first()[0]
        label = "Temp. Member Of"
    else:
        groupCount = db_ses.query(StudentGroups.id) \
            .filter(StudentGroups.id == GroupUsers.group_id, GroupUsers.user_id == user.get_id()) \
            .count()
        label = "Member Of"

    if request.method == 'GET':
        emailForm = changeEmailForm()

        return render_template(
            'dashboard/account_management.html',
            emailForm=emailForm,
            groupCount=groupCount,
            label=label,
            user=user
        )

    # POST request
    cE = changeEmailForm(request.form)
    if cE.validate_on_submit():
        address = cE.address.data
        user.update(email=address, is_static=False)
        flash(f'Account email address successfully changed to: {address}', 'success')
    else:
        flash_errors(cE)

    return redirect(url_for('dashboard.account'))


@blueprint.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    """List of all students and groups. Group, student, and instructor management forms"""
    user_is_admin()

    db_ses = db.session
    users_per_group = {}

    students = db_ses.query(User.id, User.username, User.email, User.is_static).filter(User.is_instructor == False)
    instructors = db_ses.query(User.id, User.username, User.email).filter(User.is_instructor == True)
    groups = StudentGroups.query.all()

    groupNames = [group.name for group in groups]

    for name in groupNames:
        users_per_group[name] = db_ses.query(User.id, User.username, User.email, User.is_static).filter(
            StudentGroups.name == name,
            StudentGroups.id == GroupUsers.group_id,
            GroupUsers.user_id == User.id,
        )

    if request.method == "GET":
        groupMaker = GroupForm()
        userAdder = addUsersForm()
        instructorManager = manageInstructorForm()
        groupEraser = deleteGroupForm()

        return render_template(
            "dashboard/admin.html",
            groupMaker=groupMaker,
            userAdder=userAdder,
            instructorManager=instructorManager,
            groups=groups,
            students=students,
            instructors=instructors,
            usersPGroup=users_per_group,
            groupEraser=groupEraser
        )

    # POST request
    ajax = process_request(request.form)
    if ajax:
        temp = ajax[0]
        if temp == 'utils/create_group_response.html':
            if len(ajax) == 1:
                return render_template(temp)
            elif len(ajax) < 4:
                return render_template(temp, group=ajax[1], users=ajax[2])

            return render_template(temp, group=ajax[1], users=ajax[2], pairs=ajax[3])
        elif temp == 'utils/manage_student_response.html':
            if len(ajax) == 1:
                return render_template(temp)

            return render_template(temp, group=ajax[1], users=ajax[2])

    return redirect(url_for("dashboard.admin"))


@blueprint.route("/instructor", methods=["GET", "POST"])
@login_required
def instructor():
    """List of an instructors groups"""
    user_is_instructor()

    userId = session.get("_user_id")
    db_ses = db.session

    students = db_ses.query(User.id, User.username, User.email, User.is_static).filter(User.is_instructor == False)
    groups = db_ses.query(
        StudentGroups.id, StudentGroups.name, StudentGroups.code
    ).filter(StudentGroups.owner_id == userId)
    users_per_group = {}

    for group in groups:
        users_per_group[group.name] = db_ses.query(User.id, User.username, User.email, User.is_static).filter(
            StudentGroups.name == group.name,
            StudentGroups.id == GroupUsers.group_id,
            GroupUsers.user_id == User.id,
        )

    if request.method == "GET":
        groupMaker = GroupForm()
        userAdder = addUsersForm()

        return render_template(
            "dashboard/instructor.html",
            groupMaker=groupMaker,
            userAdder=userAdder,
            students=students,
            groups=groups,
            usersPGroup=users_per_group,
        )

    # POST request
    ajax = process_request(request.form)
    if ajax:
        temp = ajax[0]
        if temp == 'utils/create_group_response.html':
            if len(ajax) == 1:
                return render_template(temp)
            elif len(ajax) < 4:
                return render_template(temp, group=ajax[1], users=ajax[2])

            return render_template(temp, group=ajax[1], users=ajax[2], pairs=ajax[3])
        elif temp == 'utils/manage_student_response.html':
            if len(ajax) == 1:
                return render_template(temp)

            return render_template(temp, group=ajax[1], users=ajax[2])

    return redirect(url_for("dashboard.instructor"))

@blueprint.route("/notification", methods=["GET", "POST"])
@login_required
def notification():
    
    # if request.method == "POST": process_request(request.form)
    notifications_raw = Notification.query.all()
    
    notifications_processed = []
    for notif in notifications_raw:
        notif_serialized = {
            "id": notif.id,
            "date": notif.date.isoformat(),
            "detail": notif.detail
        }
        notifications_processed.append(notif_serialized)

    # deleteNotify = notifyDeleteForm()
    notifications_export = json.dumps(notifications_processed)

    return render_template(
        "dashboard/notification.html",
        notifications=notifications_export
        # deleteNotify=deleteNotify
    )

@blueprint.route("/student_scenario/<i>", methods=["GET", "POST"])
@login_required
def student_scenario(i):
    if student_has_access(i):
        if scenario_exists(i):
            status, owner, desc, s_type, s_name, u_name, pw, guide, questions = tempMaker(i, "stu")
            # query = db_ses.query(User.id)\
            #    .filter(Responses.scenario_id == i).filter(Responses.user_id == User.id).all()
            uid = session.get("_user_id")
            # att = db_ses.query(Scenarios.attempt).filter(Scenarios.id == i).first()
            addresses = identify_state(s_name, status)
            # query = db_ses.query(Responses.user_id, Responses.attempt, Responses.question, Responses.points,
            #                     Responses.student_response).filter(Responses.scenario_id == i)\
            #    .filter(Responses.user_id == uid).filter(Responses.attempt == att).all()
            if request.method == "GET":
                scenarioResponder = scenarioResponseForm()
                aList = displayCorrectAnswers(s_name, uid)
                progress = displayProgress(i, uid)
                example = -1

                return render_template(
                    # "dashboard/student_scenario.html",
                    # id=i,
                    # owner=owner,
                    # desc=desc,
                    # s_type=s_type,
                    # s_name=s_name,
                    # guide=guide,
                    # questions=questions,
                    # srF=scenarioResponder,
                    # aList=aList,
                    # progress=progress,
                    # example=example
                    "dashboard/student_scenario_new.html",
                    uid = uid,
                    add=addresses,
                    status=status,
                    u_name=u_name,
                    pw=pw,
                    scenario_id=i,
                )

            # POST request
            ajax = process_request(request.form)  # scenarioResponseForm(request.form) # this validates it

            if ajax:
                return render_template(
                    "utils/student_answer_response.html",
                    progress=displayProgress(i, uid),
                    score=ajax[1]
                )

            return redirect(url_for("dashboard.student_scenario", i=i))
        
        return abort(404)

    return abort(403)


@blueprint.route("/catalog", methods=["GET"])
@login_required
def catalog():
    user_is_admin_and_instructor()

    return render_template(
        "dashboard/catalog.html",
        scenarios=populate_catalog(),
        groups=StudentGroups.query.all(),
        form=modScenarioForm(request.form)  # type2Form()
    )


@blueprint.route("/make_scenario", methods=["POST"])
@login_required
def make_scenario():
    user_is_admin_and_instructor()

    form = makeScenarioForm(request.form)  # type2Form()

    if form.validate_on_submit():
        from ..tasks import CreateScenarioTask
        db_ses = db.session
        name = request.form.get("scenario_name")
        s_type = identify_type(request.form)
        own_id = session.get("_user_id")
        group = request.form.get("scenario_group")

        students = (
            db_ses.query(User.username)
            .filter(StudentGroups.name == group)
            .filter(StudentGroups.id == GroupUsers.group_id)
            .filter(GroupUsers.user_id == User.id)
            .all()
        )

        Scenarios.create(name=name, description=s_type, owner_id=own_id)
        NotifyCapture(f"Scenario {name} has been created.")
        #Notification.create(details=something, date=something)
        s_id = db_ses.query(Scenarios.id).filter(Scenarios.name == name).first()

        s_id_list = list(s_id._asdict().values())[0]

        scenario = Scenarios.query.filter_by(id=s_id_list).first()
        scenario.update(status=7)
        g_id = db_ses.query(StudentGroups.id).filter(StudentGroups.name == group).first()
        g_id = g_id._asdict()

        # JUSTIFICATION:
        # Above queries return sqlalchemy collections.result objects
        # _asdict() method is needed in case celery serializer fails
        # Unknown exactly when this may occur, maybe version differences between Mac/Linux

        for i, s in enumerate(students):
            students[i] = s._asdict()

        # s_id, g_id = s_id._asdict(), g_id._asdict()

        gid = g_id["id"]
        student_ids = db_ses\
                    .query(GroupUsers.id)\
                    .filter(GroupUsers.group_id == gid)\
                    .all()

        namedict = gen_chat_names(student_ids, s_id_list)
        print(f"name: {name}")
        print(f"s_type: {s_type}")
        print(f"own_id: {own_id}")
        print(f"students: {students}")
        print(f"g_id: {g_id}")
        print(f"s_id_list: {s_id_list}")
        print(f"namedict: {namedict}")
        CreateScenarioTask.delay(name, s_type, own_id, students, g_id, s_id_list, namedict)
        flash(
            "Success! Your scenario will appear shortly. This page will automatically update. " \
            f"Students found: {students}",
            "success"
        )
    else:
        flash_errors(form)

    return redirect(url_for("dashboard.scenarios"))


@blueprint.route("/scenarios", methods=["GET", "POST"])
@login_required
def scenarios():
    """List of scenarios and scenario controls."""
    user_is_admin_and_instructor()

    scenarioModder = modScenarioForm()  # type2Form()
    scenarios = Scenarios.query.all()
    groups = StudentGroups.query.all()

    if request.method == "GET":
        return render_template(
            "dashboard/scenarios.html",
            scenarios=scenarios,
            scenarioModder=scenarioModder,
            groups=groups,
        )

    # POST request
    process_request(request.form)

    return render_template(
        "dashboard/scenarios.html",
        scenarios=scenarios,
        scenarioModder=scenarioModder,
        groups=groups,
    )


@blueprint.route("/scenarios/<sId>")
def scenariosInfo(sId):
    user_is_admin_and_instructor()

    status, owner, bTime, desc, s_type, s_name, guide, questions = tempMaker(sId, "ins")
    addresses = identify_state(s_name, status)
    db_ses = db.session
    query = db_ses.query(Responses.id, Responses.user_id, Responses.attempt, Responses.points,
                         Responses.question, Responses.student_response, Responses.scenario_id, User.username)\
        .filter(Responses.scenario_id == sId).filter(Responses.user_id == User.id).all()
    resp = queryPolish(query, s_name)
    try:
        logData = readCSV(sId, 'id')
        print(logData)
    except FileNotFoundError:
        flash(f"Log file '{s_name}.csv' was not found, has anyone played yet?")
        logData = []

    gid = db_ses.query(StudentGroups.id).filter(Scenarios.id == sId, ScenarioGroups.scenario_id == Scenarios.id, ScenarioGroups.group_id == StudentGroups.id).first()[0]

    players = db_ses.query(User.username).filter(GroupUsers.group_id == StudentGroups.id, StudentGroups.id == gid, GroupUsers.user_id == User.id).all()

    u_logs = groupCSV(logData, 4)  # Make dictionary using 6th value as key (player name)

    return render_template(
        "dashboard/scenarios_info.html",
        i=sId,
        s_type=s_type,
        desc=desc,
        status=status,
        owner=owner,
        dt=bTime,
        s_name=s_name,
        add=addresses,
        guide=guide,
        questions=questions,
        resp=resp,
        rc=logData, # rc may not be needed with individual user logs in place
        players=players,
        u_logs=u_logs
    )


@blueprint.route("/scenarios/<sId>/<rId>")
@login_required
def scenarioResponse(sId, rId):
    user_is_admin_and_instructor()

    if scenario_exists(sId):
        d = responseSelector(rId)
        u_id, uName, s_id, sName, aNum = responseProcessing(d)
        # s_type = db_ses.query(Scenarios.description).filter(Scenarios.id == s_id).first()
        query = db.session.query(Responses.id, Responses.user_id, Responses.attempt, Responses.question,
                                Responses.points, Responses.student_response, User.username)\
            .filter(Responses.scenario_id == sId).filter(Responses.user_id == User.id).filter(Responses.attempt == aNum).all()
        table = getResponses(u_id, aNum, query, questionReader(sName))
        score = getScore(u_id, aNum, query, questionReader(sName))

        return render_template(
            "dashboard/scenario_response.html",
            i=sId,
            u_id=u_id,
            uName=uName,
            s_id=s_id,
            sName=sName,
            aNum=aNum,
            table=table,
            scr=score
        )

    return abort(404)


@blueprint.route("/scenarios/<sId>/graphs/<user>")
@login_required
def scenarioGraph(sId, user):
    user_is_admin_and_instructor()

    if scenario_exists(sId):
        scenario = db.session.query(Scenarios.name).filter(Scenarios.id == sId).first()[0]
        graph = getGraph(scenario, user)

        if graph:
            return render_template("dashboard/graphs.html", graph=graph)

        flash(f"Graph for {user} in scenario {scenario} could not be opened.")
        return redirect(url_for('dashboard.scenariosInfo', i=sId))

    return abort(404)


@blueprint.route("/scenarios/<scenarioId>/getLogs")
@login_required
def getLogs(scenarioId):
    admin, instructor = get_roles()

    if not admin or not instructor:
        return abort(403)

    db_ses = db.session
    scenario_exists = db_ses.query(Scenarios).get(scenarioId)

    if scenario_exists is None:
        flash(f"Scenario with ID {scenarioId} could not be found")
        return redirect(url_for('dashboard.scenarios'))

    scenario = db_ses.query(Scenarios.name).filter(Scenarios.id == scenarioId).first()[0]

    logs = f"./data/tmp/{scenario}/{scenario}-history.csv"

    if os.path.isfile(logs):
        logs, fname = logs.rsplit('/', 1)    # ./data/tmp/ScenarioName/, ScenarioName-history.csv

        return send_from_directory(f".{logs}", fname, as_attachment=True)

    flash(f"Log file for scenario {scenario} could not be found")
    return redirect(url_for('dashboard.scenariosInfo', i=scenarioId))


@blueprint.route("/set_view", methods=["GET"])
@login_required
def set_view():
    if check_role_view(request.args["mode"]):
        session["viewMode"] = request.args["mode"]
    else:
        session.pop("viewMode", None)

    return redirect(url_for("public.home"))

