
from flask_login import login_user, logout_user

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

from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    g,  ## see note
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
blueprint_edurange3_instructor = Blueprint('edurange3_instructor',__name__, url_prefix='/edurange3/api')
csrf_protect.exempt(blueprint_edurange3_instructor) # disables legacy csrf_protect interference; enforced elsewhere

@blueprint_edurange3_instructor.errorhandler(418)
def custom_error_handler(error):
    response = jsonify({"error": "request denied"})
    response.status_code = 418
    response.content_type = "application/json"
    return response

@blueprint_edurange3_instructor.route("/instructor_test")
@jwt_and_csrf_required
def instructor_test():
    current_username = g.current_username
    current_user_id = g.current_user_id
    current_user_role = g.current_user_role
    return jsonify ({"message":"this is /instructor_test"})

@blueprint_edurange3_instructor.route("/create_scenario")
@jwt_and_csrf_required
def create_scenario():
    current_username = g.current_username
    current_user_id = g.current_user_id
    current_user_role = g.current_user_role
    return jsonify ({"message":"this is /create_scenario"})