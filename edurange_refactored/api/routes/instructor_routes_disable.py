
from flask_login import login_user, logout_user
from flask import (
    Blueprint,
    request,
    session,
    jsonify,
    make_response,
    render_template,
)
from edurange_refactored.user.models import User
from edurange_refactored.extensions import db, csrf_protect
from edurange_refactored.api.utils.db_devHelper import (
    get_user,
    get_users,
    get_groups,
    get_group_users,
    get_scenarios,
    get_scenario_groups,
    get_student_responses,
    get_instructor_data,  # gets all the previous
)

import secrets
from marshmallow import ValidationError
from edurange_refactored.api.schemas.ma_user import LoginSchema
from flask_jwt_simple import create_jwt
from datetime import datetime, timedelta 

db_ses = db.session
edurange3_csrf = secrets.token_hex(32)
blueprint_edurange3_instructor = Blueprint('edurange3_instructor', __name__)
csrf_protect.exempt(blueprint_edurange3_instructor) # disables legacy csrf_protect interference; enforced elsewhere


@blueprint_edurange3_instructor.route("/edurange3/api/instructor_test")
def instructor_test():
    return jsonify ({"message":"this is /edurange3/api/instructor_test"})
