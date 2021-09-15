# -*- coding: utf-8 -*-
"""User views."""
import os
from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app,
    send_from_directory
)
from flask_login import login_required

from edurange_refactored.extensions import db
from edurange_refactored.user.forms import (
    GroupForm,
    addUsersForm,
    makeScenarioForm,
    manageInstructorForm,
    modScenarioForm,
    changeEmailForm,
    deleteGroupForm,
    scenarioResponseForm,
    showProgressForm
)

from ..form_utils import process_request
from ..scenario_utils import identify_state, identify_type, populate_catalog
from ..tasks import CreateScenarioTask
from ..utils import (
    check_role_view,
    checkAuth,
    flash_errors,
    tempMaker,
    responseProcessing,
    responseQuery,
    responseSelector,
    queryPolish,
    questionReader,
    # getScore,
    score,
    displayCorrect,
    displayProgress
)
from ..role_utils import check_admin, check_instructor, check_privs, checkEx, return_roles, checkEnr
from ..graph_utils import getGraph
from ..csv_utils import readCSV, groupCSV
from ..graphing import custom_csv_utility, graph_util
import graphviz as gv

import logging

from .models import (
    GroupUsers, 
    ScenarioGroups, 
    Scenarios, 
    StudentGroups, 
    User, 
    Responses,
    BashHistory
)

blueprint = Blueprint(
    "dashboard", __name__, url_prefix="/dashboard", static_folder="../static"
)


@blueprint.route("/set_view", methods=["GET"])
@login_required
def set_view():
    if check_role_view(request.args["mode"]):
        session["viewMode"] = request.args["mode"]
        return redirect(url_for("public.home"))
    else:
        session.pop("viewMode", None)
        return redirect(url_for("public.home"))


@blueprint.route("/account_management", methods=['GET', 'POST'])
@login_required
def account():
    db_ses = db.session
    curId = session.get('_user_id')

    user = db_ses.query(User).filter(User.id == curId).first()
    if user.is_admin or user.is_instructor:
        groupCount = db_ses.query(StudentGroups.id).filter(StudentGroups.owner_id == user.get_id()).count()
        label = "Owner Of"
    elif user.is_static:
        # In this case, groupCount is the name of the group this user is a static member of
        groupCount = db_ses.query(StudentGroups.name)\
            .filter(StudentGroups.id == GroupUsers.group_id, GroupUsers.user_id == user.get_id()).first()[0]
        label = "Temp. Member Of"
    else:
        groupCount = db_ses.query(StudentGroups.id)\
            .filter(StudentGroups.id == GroupUsers.group_id, GroupUsers.user_id == user.get_id()).count()
        label = "Member Of"

    if request.method == 'GET':
        emailForm = changeEmailForm()
        return render_template('dashboard/account_management.html', user=user, groupCount=groupCount, label=label, emailForm=emailForm)

    elif request.method == 'POST':
        cE = changeEmailForm(request.form)
        if cE.validate_on_submit():
            address = cE.address.data
            user.update(email=address, is_static=False)
            flash('Account Email address successfully changed to: {0}'.format(address), 'success')
        else:
            flash_errors(cE)

        return redirect(url_for('dashboard.account'))


@blueprint.route("/")
@login_required
def student():
    """List members."""
    # Queries for the user dashboard
    db_ses = db.session
    curId = session.get("_user_id")

    userInfo = db_ses.query(User.id, User.username, User.email).filter(User.id == curId)

    groups = (
        db_ses.query(StudentGroups.id, StudentGroups.name, GroupUsers)
        .filter(GroupUsers.user_id == curId)
        .filter(GroupUsers.group_id == StudentGroups.id)
    )

    scenarioTable = (
        db_ses.query(
            Scenarios.id,
            Scenarios.name.label("sname"),
            Scenarios.description.label("type"),
            StudentGroups.name.label("gname"),
            User.username.label("iname"),
        )
        .filter(GroupUsers.user_id == curId)
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


@blueprint.route("/student_scenario/<i>", methods=["GET", "POST"])
@login_required
def student_scenario(i):
    # i = scenario_id
    # db_ses = db.session
    if checkEnr(i):
        if checkEx(i):
            status, owner, desc, s_type, s_name, u_name, pw, guide, questions = tempMaker(i, "stu")
            # db_ses = db.session
            # query = db_ses.query(User.id)\
            #    .filter(Responses.scenario_id == i).filter(Responses.user_id == User.id).all()
            uid = session.get("_user_id")
            # att = db_ses.query(Scenarios.attempt).filter(Scenarios.id == i).first()
            addresses = identify_state(s_name, status)
            example = None
            # query = db_ses.query(Responses.user_id, Responses.attempt, Responses.question, Responses.points,
            #                     Responses.student_response).filter(Responses.scenario_id == i)\
            #    .filter(Responses.user_id == uid).filter(Responses.attempt == att).all()
            if request.method == "GET":
                scenarioResponder = scenarioResponseForm()
                aList = displayCorrect(s_name, u_name)
                progress = displayProgress(i, uid)
                return render_template("dashboard/student_scenario.html",
                                       id=i,
                                       status=status,
                                       owner=owner,
                                       desc=desc,
                                       s_type=s_type,
                                       s_name=s_name,
                                       u_name=u_name,
                                       pw=pw,
                                       add=addresses,
                                       guide=guide,
                                       questions=questions,
                                       srF=scenarioResponder,
                                       aList=aList,
                                       example=example,
                                       progress=progress)

            elif request.method == "POST":
                ajax = process_request(request.form)  # scenarioResponseForm(request.form) # this validates it
                progress = displayProgress(i, uid)
                if ajax:
                    return render_template("utils/student_answer_response.html", score=ajax[1], progress=progress)

                else:
                    return redirect(url_for("dashboard.student_scenario", i=i))
        else:
            return abort(404)
    else:
        return abort(403)

# ---- scenario routes


@blueprint.route("/catalog", methods=["GET"])
@login_required
def catalog():
    check_privs()
    scenarios = populate_catalog()
    groups = StudentGroups.query.all()
    scenarioModder = modScenarioForm(request.form)  # type2Form()  #

    return render_template(
        "dashboard/catalog.html", scenarios=scenarios, groups=groups, form=scenarioModder
    )


@blueprint.route("/make_scenario", methods=["POST"])
@login_required
def make_scenario():
    check_privs()
    form = makeScenarioForm(request.form)  # type2Form()  #
    if form.validate_on_submit():
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
        s_id = db_ses.query(Scenarios.id).filter(Scenarios.name == name).first()
        scenario = Scenarios.query.filter_by(id=s_id).first()
        scenario.update(status=7)
        g_id = (
            db_ses.query(StudentGroups.id).filter(StudentGroups.name == group).first()
        )

        # JUSTIFICATION:
        # Above queries return sqlalchemy collections.result objects
        # _asdict() method is needed in case celery serializer fails
        # Unknown exactly when this may occur, maybe version differences between Mac/Linux

        for i, s in enumerate(students):
            students[i] = s._asdict()
        s_id = s_id._asdict()
        g_id = g_id._asdict()

        CreateScenarioTask.delay(name, s_type, own_id, students, g_id, s_id)
        flash(
            "Success, your scenario will appear shortly. This page will automatically update. Students Found: {}".format(
                students
            ),
            "success",
        )
    else:
        flash_errors(form)

    return redirect(url_for("dashboard.scenarios"))


@blueprint.route("/scenarios", methods=["GET", "POST"])
@login_required
def scenarios():
    """List of scenarios and scenario controls"""
    check_privs()
    scenarioModder = modScenarioForm()  # type2Form()  #
    scenarios = Scenarios.query.all()
    groups = StudentGroups.query.all()

    if request.method == "GET":
        return render_template(
            "dashboard/scenarios.html",
            scenarios=scenarios,
            scenarioModder=scenarioModder,
            groups=groups,
        )

    elif request.method == "POST":
        process_request(request.form)
        return render_template(
            "dashboard/scenarios.html",
            scenarios=scenarios,
            scenarioModder=scenarioModder,
            groups=groups,
        )


@blueprint.route("/scenarios/<i>")
def scenariosInfo(i):
    # i = scenario_id
    admin, instructor = return_roles()
    if not admin and not instructor:
        return abort(403)

    status, owner, bTime, desc, s_type, s_name, guide, questions = tempMaker(i, "ins")
    addresses = identify_state(s_name, status)
    db_ses = db.session
    query = db_ses.query(Responses.id, Responses.user_id, Responses.attempt, Responses.points,
                         Responses.question, Responses.student_response, Responses.scenario_id, User.username)\
        .filter(Responses.scenario_id == i).filter(Responses.user_id == User.id).all()
    resp = queryPolish(query, s_name)
    try:
        rc = readCSV(i)
    except FileNotFoundError:
        flash("Log file '{0}.csv' was not found, has anyone played yet? - ".format(s_name))
        rc = []

    gid = db_ses.query(StudentGroups.id).filter(Scenarios.id == i, ScenarioGroups.scenario_id ==
                                                Scenarios.id, ScenarioGroups.group_id == StudentGroups.id).first()
    players = db_ses.query(User.username).filter(GroupUsers.group_id == StudentGroups.id,
                                                 StudentGroups.id == gid, GroupUsers.user_id == User.id).all()

    u_logs = groupCSV(rc, 4)  # make dictionary using 6th value as key (player name)

    return render_template("dashboard/scenarios_info.html",
                           i=i,
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
                           rc=rc,  # rc may not be needed with individual user logs in place
                           players=players,
                           u_logs=u_logs)


@blueprint.route("/scenarios/<i>/<r>")
def scenarioResponse(i, r):
    # i = scenario_id, r = responses id
    if checkAuth(i):
        if checkEx(i):
            db_ses = db.session
            d = responseSelector(r)
            u_id, uName, s_id, sName, aNum = responseProcessing(d)
            # s_type = db_ses.query(Scenarios.description).filter(Scenarios.id == s_id).first()
            query = db_ses.query(Responses.id, Responses.user_id, Responses.attempt, Responses.question,
                                 Responses.points, Responses.student_response, User.username)\
                .filter(Responses.scenario_id == i).filter(Responses.user_id == User.id).filter(Responses.attempt == aNum).all()
            table = responseQuery(u_id, aNum, query, questionReader(sName))
            # score(getScore(u_id, aNum, query), questionReader(sName))
            scr = score(u_id, aNum, query, questionReader(sName))

            return render_template("dashboard/scenario_response.html",
                                   i=i,
                                   u_id=u_id,
                                   uName=uName,
                                   s_id=s_id,
                                   sName=sName,
                                   aNum=aNum,
                                   table=table,
                                   scr=scr)
        else:
            return abort(404)
    else:
        return abort(403)


@blueprint.route("/scenarios/<i>/graphs/<u>")
def scenarioGraph(i, u):
    # i = scenario_id, u = username
    if checkAuth(i):
        if checkEx(i):
            db_ses = db.session
            scenario = db_ses.query(Scenarios.name).filter(Scenarios.id == i).first()[0]
            graph = getGraph(scenario, u)
            if graph:
                return render_template("dashboard/graphs.html", graph=graph)
            else:
                flash("Graph for {0} in scenario {1} could not be opened.".format(u, scenario))
                return redirect(url_for('dashboard.scenariosInfo', i=i))

        else:
            return abort(404)
    else:
        return abort(403)


@blueprint.route("/scenarios/<i>/getLogs")
def getLogs(i):
    # i = scenario_id
    admin, instructor = return_roles(i)

    if not admin or not instructor:
        return abort(403)

    db_ses = db.session
    id_test = db_ses.query(Scenarios).get(id)

    if id_test is None:
        flash("Scenario with ID # {0} could not be found".format(i))
        redirect(url_for('dashboard.scenarios'))

    scenario = db_ses.query(Scenarios.name).filter(Scenarios.id == i).first()[0]

    logs = "./data/tmp/" + scenario + "/" + scenario + "-history.csv"
    if os.path.isfile(logs):
        logs = "." + logs
        fname = logs.rsplit('/', 1)[-1]  # 'ScenarioName-history.csv'
        logs = logs.rsplit('/', 1)[0]  # '../data/tmp/ScenarioName/'
        return send_from_directory(logs, fname, as_attachment=True)

    else:
        flash("Log file for scenario {0} could not be found.".format(scenario))
        return redirect(url_for('dashboard.scenariosInfo', i=i))


# -----


@blueprint.route("/instructor", methods=["GET", "POST"])
@login_required
def instructor():
    """List of an instructors groups"""
    check_instructor()
    # Queries for the owned groups table
    curId = session.get("_user_id")
    db_ses = db.session

    students = db_ses.query(User.id, User.username, User.email, User.is_static).filter(User.is_instructor == False)
    groups = db_ses.query(
        StudentGroups.id, StudentGroups.name, StudentGroups.code
    ).filter(StudentGroups.owner_id == curId)
    users_per_group = {}

    for g in groups:
        users_per_group[g.name] = db_ses.query(User.id, User.username, User.email, User.is_static).filter(
            StudentGroups.name == g.name,
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

    elif request.method == "POST":
        ajax = process_request(request.form)
        if ajax:
            temp = ajax[0]
            if temp == 'utils/create_group_response.html':
                if len(ajax) == 1:
                    return render_template(temp)
                elif len(ajax) < 4:
                    return render_template(temp, group=ajax[1], users=ajax[2])
                else:
                    return render_template(temp, group=ajax[1], users=ajax[2], pairs=ajax[3])
            elif temp == 'utils/manage_student_response.html':
                if len(ajax) == 1:
                    return render_template(temp)
                else:
                    return render_template(temp, group=ajax[1], users=ajax[2])
        else:
            return redirect(url_for("dashboard.instructor"))


@blueprint.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    """List of all students and groups. Group, student, and instructor management forms"""
    check_admin()
    db_ses = db.session
    # Queries for the tables of students and groups
    students = db_ses.query(User.id, User.username, User.email, User.is_static).filter(User.is_instructor == False)
    instructors = db_ses.query(User.id, User.username, User.email).filter(User.is_instructor == True)
    groups = StudentGroups.query.all()
    groupNames = []
    users_per_group = {}

    for g in groups:
        groupNames.append(g.name)

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

    elif request.method == "POST":
        ajax = process_request(request.form)
        if ajax:
            temp = ajax[0]
            if temp == 'utils/create_group_response.html':
                if len(ajax) == 1:
                    return render_template(temp)
                elif len(ajax) < 4:
                    return render_template(temp, group=ajax[1], users=ajax[2])
                else:
                    return render_template(temp, group=ajax[1], users=ajax[2], pairs=ajax[3])
            elif temp == 'utils/manage_student_response.html':
                if len(ajax) == 1:
                    return render_template(temp)
                else:
                    return render_template(temp, group=ajax[1], users=ajax[2])
        else:
            return redirect(url_for("dashboard.admin"))


@blueprint.route("/progress_dev", methods=["GET", "POST"])
def progress_update_dev():
    check_instructor()
    logging.basicConfig(level=logging.DEBUG)
    log = current_app.logger

    db_ses = db.session

    # IDEAL TO USE ONLY DB QUERY TO AQUIRE ALL DATA NO MORE CSV READING...
    # data = db_ses.query(BashHistory.input, BashHistory.tag).filter(Scenarios.description == "FileWrangler").all()

    form = showProgressForm(request.form)

    students = db_ses.query(User.username).filter(User.is_instructor==False, User.is_admin==False)
    students = [s[0] for s in students]
    # active_scenarios = db_ses.query(Scenarios.name).filter(Scenarios.description in ['FileWrangler', 'GettingStarted']).all()
    active_scenarios = db_ses.query(Scenarios.name).all()
    active_scenarios = [i[0] for i in active_scenarios]
    # TODO only return Getting_started and file_wrangler to dropdown menu
    # filter(Scenarios.description == 'Getting_Started',Scenarios.description == File_Wrangler')

    if request.method == 'POST':
        def refresh_options_html(target_selection, items):
            fresh_options = '<option>select</option>'
            for i in items:
                if i == target_selection:
                    fresh_options += f'<option selected>{i}</option>'
                else:
                    fresh_options += f'<option>{i}</option>'
            return fresh_options

        source_val = request.form.get('source_val', -1)
        source_id = request.form.get('source_id')
        log.info(f'source selector: {source_id}')

        target_selection = request.form.get('target_selection')
        log.info(f'target selection: {target_selection}')
        if request.form.get('dropdown_update', False):
            if source_id == '#student-select':
                if source_val == 'select':
                    return refresh_options_html(target_selection, active_scenarios)
                student_username = source_val
                log.info(f'source selector value: {source_val}')
                student_scenarios = db_ses.query(
                    Scenarios.name).filter(
                        student_username == User.username,
                        User.id == GroupUsers.user_id,
                        GroupUsers.group_id == StudentGroups.id,
                        StudentGroups.id == ScenarioGroups.group_id,
                        ScenarioGroups.scenario_id == Scenarios.id).all()
                student_scenarios = [s[0] for s in student_scenarios]
                log.info(f"scenarios for {student_username}: {student_scenarios}")
                return refresh_options_html(target_selection, student_scenarios)

            elif source_id == '#scenario-select':
                if source_val == 'select':
                    return refresh_options_html(target_selection, students)
                scenario_name = source_val
                log.info(source_val)
                scenario_students = db_ses.query(
                    User.username).filter(
                        scenario_name == Scenarios.name,
                        Scenarios.id == ScenarioGroups.scenario_id,
                        ScenarioGroups.group_id == StudentGroups.id,
                        StudentGroups.id == GroupUsers.group_id,
                        GroupUsers.user_id == User.id,
                        User.is_admin == False,
                        User.is_instructor == False).all()
                scenario_students = [s[0] for s in scenario_students]
                log.info(f"students in {scenario_name}: {scenario_students}")
                return refresh_options_html(target_selection, scenario_students)
        else: 
            selected_scenario = request.form.get('scenario') #TODO rename to singular scenario
            scenario_type = db_ses.query(Scenarios.description).filter(Scenarios.name == selected_scenario).all()[0][0]

            student_uname = request.form.get('student')
            
            log.info('selected scenario: ' + str(selected_scenario))
            log.info(f'selected sc type: {scenario_type}')
            # selected_student = request.form.keys()
            # log.info(selected_student)
            data = db_ses.query(
                BashHistory.prompt, 
                BashHistory.tag,
                BashHistory.timestamp, 
                BashHistory.input).filter(
                    BashHistory.container_name == scenario_type,
                    BashHistory.prompt.contains(student_uname)).all()
            # all_data = db_ses.query

            log.info(data)
            # for entry in data:
            #     log.info(entry)
            # for obj in data:
            #     obj_dict = obj.__dict__
            #     for k in obj_dict.keys():
            #         log.info(obj_dict[k])

            # data = db_ses.query(BashHistory).filter()
            # SIMPLE TEST CASE IF SOMETHING IS WRONG...
            # WILL BE REMOVED LATER
            # chart_data = gv.Graph(comment='simple test', format='svg')
            # chart_data.node('H', label='Hello')
            # chart_data.node('G', label='Graphviz')
            # chart_data.edge('H', 'G', label='morphism')

            # replace this with query info
            # log = custom_csv_utility.file_load("sample_data.csv")

            student_log = custom_csv_utility.db_log_load(data, scenario_type)

            log.info(f'student log: ')
            for item in student_log:
                log.info(item)
            test_report = graph_util.Report(student_log)
            graph_data = test_report.get_graph()        
            graph_output = graph_data.pipe(format='svg').decode('utf-8')

            return render_template("dashboard/progress_dev.html", form=form, students=students, scenarios=active_scenarios, graph_output=graph_output)

    else:
        return render_template("dashboard/progress_dev.html", form=form, scenarios=active_scenarios, students=students, graph_output='')
