
from flask_login import login_user, logout_user
from edurange_refactored.extensions import db, csrf_protect
from edurange_refactored.user.models import (
    User,
    GroupUsers,
    ScenarioGroups,
    Scenarios,
    StudentGroups,
    Responses,
    Notification
)
from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    g, # see note
)
from ..utils.auth_utils import jwt_and_csrf_required
from edurange_refactored.role_utils import user_is_admin_and_instructor

# -*- coding: utf-8 -*-
"""User views."""
import os
import json
from datetime import datetime

from edurange_refactored.extensions import db
from edurange_refactored.notification_utils import NotifyCapture
from edurange_refactored.user.forms import (
    
    makeScenarioForm,
 
)
from edurange_refactored.tasks import CreateScenarioTask

from edurange_refactored.user.models import GroupUsers, Scenarios, StudentGroups, User

#######
# The `g` object is a global flask object that lasts ONLY for the life of a single request.
#
# The following values are populated when the jwt_and_csrf_required() function is invoked,
# if the request passes auth:
#   g.current_username
#   g.current_user_id
#   g.current_user_role
#
# You must import the `g` object from Flask, which will be the same instance of `g` as first 
# accessed by jwt_and_csrf_required().
# 
# You must also import jwt_and_csrf_required() from auth_utils.py and include it as a decorator
# on any route where those values would be needed (i.e., an auth protected route)
#
# The values will then be available to routes that use the @jwt_and_csrf_required decorator.
#
# To ensure no accidental auth 'misses', always use these 3 variables to obtain these values, 
# rather than parsing the values yourself by way of request body or directly from the JWT.  
# That way, the values will always return null if the request hasn't been fully authenticated 
# (i.e. if you forgot to use the decorator).
#######

db_ses = db.session
blueprint_edurange3_student = Blueprint(
    'edurange3_student', 
    __name__, 
    url_prefix='/edurange3/api')

csrf_protect.exempt(blueprint_edurange3_student) # disables legacy csrf_protect interference; enforced elsewhere

@blueprint_edurange3_student.errorhandler(418)
def custom_error_handler(error):
    response = jsonify({"error": "request denied"})
    response.status_code = 418
    response.content_type = "application/json"
    return response

@blueprint_edurange3_student.route("/logout", methods=["POST"])
@jwt_and_csrf_required
def logout():
    current_username = g.current_username
    logout_user()

    response_data = {"message": f"User {current_username} has been successfully logged out."}
    response = make_response(jsonify(response_data))

    response.set_cookie('edurange3_jwt', '', expires=0, samesite='Lax', httponly=True, path='/edurange3/')
    response.set_cookie('X-XSRF-TOKEN', '', expires=0, samesite='Lax', path='/edurange3/')
    
    return response

@blueprint_edurange3_student.route('/jwt_test', methods=['GET']) # DEV_ONLY
@jwt_and_csrf_required
def jwt_test():
    current_username = g.current_username
    current_user_id = g.current_user_id
    current_user_role = g.current_user_role

    return jsonify({
        'message': 'Welcome',
        'username': current_username,
        'user_id' : current_user_id,
        'user_role': current_user_role
    })

@blueprint_edurange3_student.route('/groups', methods=['GET']) # DEV_ONLY
@jwt_and_csrf_required
def get_groups():
    db_ses = db.session 
    all_groups = db_ses.query(StudentGroups).all()
    all_groups_list = []

    for group in all_groups:
        group_info = {
            "id": group.id,
            "name": group.name,
            "owner_id": group.owner_id,
            "code": group.code,
            "hidden": group.hidden,
        }
    print(jsonify(all_groups_list))
    print(all_groups_list)
    all_groups_list.append(group_info)
    return jsonify(all_groups_list)
    

@blueprint_edurange3_student.route("/make_scenario", methods=["POST"])
@jwt_and_csrf_required
def make_scenario():
    
    user_is_admin_and_instructor()

    db_ses = db.session
    name = request.form.get("scenario_name")
    '''

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

        Scenarios.create(name=name, description=s_type, owner_id=own_id) #creates database entry
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

        CreateScenarioTask.delay(name, s_type, own_id, students, g_id, s_id_list, namedict)
        flash(
            "Success! Your scenario will appear shortly. This page will automatically update. " \
            f"Students found: {students}",
            "success"
        )
        '''
    return jsonify({
        'scenario_name': name,
    })

 
        
    
@blueprint_edurange3_student.route('/get_guide', methods=['GET']) # WIP
@jwt_and_csrf_required
def get_guide():
    current_username = g.current_username
    current_user_id = g.current_user_id
    current_user_role = g.current_user_role

    # get unique data for scenario instance (SSH info, randomized answer stuff, etc)

    # get user-scenario data (answers, ... )


    return jsonify({
        'message': 'Welcome',
        'username': current_username,
        'user_id' : current_user_id,
        'user_role': current_user_role
    })
