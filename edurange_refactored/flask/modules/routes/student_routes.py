
from flask_login import login_user, logout_user
from flask import (
    Blueprint,
    request,
    session,
    jsonify,
    make_response,
    render_template,
    g
)
from edurange_refactored.user.models import User
from edurange_refactored.extensions import db, csrf_protect
from edurange_refactored.flask.modules.utils.db_devHelper import (
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
from edurange_refactored.flask.modules.db.schemas.ma_user import LoginSchema
from flask_jwt_simple import create_jwt
from datetime import datetime, timedelta 
from ..utils.auth_utils import jwt_and_csrf_required

db_ses = db.session
edurange3_csrf = secrets.token_hex(32)
blueprint_edurange3_student = Blueprint('edurange3_student', __name__)
csrf_protect.exempt(blueprint_edurange3_student) # disables legacy csrf_protect interference; enforced elsewhere

@blueprint_edurange3_student.route("/edurange3/api/student_test")
def student_test():
    return jsonify ({"message":"this is /edurange3/api/student_test"})

blueprint_edurange3_student = Blueprint('edurange3_student', __name__)
csrf_protect.exempt(blueprint_edurange3_student) # disables legacy csrf_protect interference; enforced elsewhere

@blueprint_edurange3_student.route("/edurange3/dashboard/jwt_auth", methods=["POST"]) # DEV_ONLY
@jwt_and_csrf_required
def jwt_auth():
    decoded = g.decoded_jwt_token   
    return jsonify({"message": f"Welcome {decoded['sub']}"})