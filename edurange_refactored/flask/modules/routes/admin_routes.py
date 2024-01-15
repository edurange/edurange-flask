
import time
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
from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    session,
    g, ## see note
)
from ..utils.auth_utils import jwt_and_csrf_required

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
blueprint_edurange3_admin = Blueprint('edurange3_admin', __name__, url_prefix='/edurange3/api')
csrf_protect.exempt(blueprint_edurange3_admin) # csrf imposed elsewhere (see below)

@blueprint_edurange3_admin.errorhandler(418)
def custom_error_handler(error):
    response = jsonify({"error": "request denied"})
    response.status_code = 418
    response.content_type = "application/json"
    return response

@blueprint_edurange3_admin.route("/admin_test")
@jwt_and_csrf_required
def admin_test():
    current_username = g.current_username
    current_user_id = g.current_user_id
    current_user_role = g.current_user_role
    return jsonify ({"message":"this is /admin_test"})

@blueprint_edurange3_admin.route("/generate_registration_code", methods=["POST"])
@jwt_and_csrf_required
def generate_registration_code():
    current_username = g.current_username
    current_user_id = g.current_user_id
    current_user_role = g.current_user_role

    if current_user_role != "admin":
        return jsonify({"error":"request denied"})
    
    minsUntilExpire = 90
    if "minsUntilExpire" in request.json:
        minsUntilExpire = request.json["minsUntilExpire"]
    secsUntilExpire = minsUntilExpire * 60
    expiry = time.time() + secsUntilExpire

    session['registration_code'] = secrets.token_hex(32)
    session['registration_code_expiry'] = expiry
    
    genCode = secrets.token_urlsafe(8)

    return jsonify ({"registration_code": genCode, "expiry":expiry})