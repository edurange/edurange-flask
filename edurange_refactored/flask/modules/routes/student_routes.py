
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
