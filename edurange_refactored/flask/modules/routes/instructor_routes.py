
from flask_login import login_user, logout_user
from edurange_refactored.user.models import User, StudentGroups, Scenarios
from edurange_refactored.extensions import db, csrf_protect
from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    g,  ## see note
)
from ..utils.auth_utils import jwt_and_csrf_required, instructor_only
from ..utils.instructor_utils import generateTestAccts
from werkzeug.exceptions import abort
from ..utils.scenario_interface import scenario_create, list_all_scenarios

from ..utils.instructor_utils import generate_registration_code as grc
from edurange_refactored.user.forms import changeEmailForm

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
    instructor_only()
    return jsonify ({"message":"this is /instructor_test"})

@blueprint_edurange3_instructor.route("/create_group")
@jwt_and_csrf_required
def create_group():

    # work in progress
    
    reqJSON = request.json


    current_username = g.current_username
    current_user_id = g.current_user_id
    current_user_role = g.current_user_role

    if current_user_role == 'instructor' or current_user_role == 'admin':
        # allowed
        code = grc()
        group_name = reqJSON['group_name'] # something like this
        
        #group_obj is created if postgres succesfully makes entry
        group_obj = StudentGroups.create(name=group_name, owner_id=current_user_id, code=code)
    else: abort(403)

    return jsonify ({"message":f"userGroup {group_name} created"})

@blueprint_edurange3_instructor.route("/generate_users")
@jwt_and_csrf_required
def generate_users():

    # work in progress ;
    
    reqJSON = request.json

    current_username = g.current_username
    current_user_id = g.current_user_id
    current_user_role = g.current_user_role

    if current_user_role == 'instructor' or current_user_role == 'admin':
        generatedUsers = generateTestAccts(reqJSON['new_user_count'], reqJSON['group_name'])

    else: abort(403)

    return jsonify ({"message":f"{reqJSON['new_user_count']} users for group {reqJSON['group_name']} created"})

@blueprint_edurange3_instructor.route("/scenario_interface", methods=["POST"])
@jwt_and_csrf_required
def scenario_interface():
    instructor_only()

    requestJSON = request.json
    if ('METHOD' not in requestJSON):
        return jsonify({'message':'method not found'})
        abort(418)

    method = requestJSON['METHOD']
    if method not in ('LIST','CREATE', 'START', 'STOP', 'UPDATE', 'DELETE'):
        return jsonify({'message':'wrong method given'})
        abort(418)

    def list_scenarios(requestJSON):
        print("Performing LIST method")
        scenario_list = list_all_scenarios(requestJSON)
        return scenario_list

    def create_scenario(requestJSON):   
        print("Performing CREATE method")
        if ("type" not in requestJSON or "name" not in requestJSON):
            abort(418)
        scenario_type = requestJSON["type"]
        scenario_name = requestJSON["name"]
        scenario_group_name = "goob"
        # scenario_group_name = requestJSON["Group"]
        scenario_users = scenario_create(scenario_type, scenario_name, scenario_group_name)
        if (scenario_users != None):
            print("CREATE method success")
            return scenario_users
        else: 
            print ("Scenario CREATE failed")
            return None


    def start_scenario(requestJSON):
        print("Performing START method")

    def stop_scenario(requestJSON):
        print("Performing STOP method")

    def update_scenario(requestJSON):
        print("Performing UPDATE method")

    def delete_scenario(requestJSON):
        print("Performing DELETE method")

    method_switch = {
        "LIST": list_scenarios,
        "CREATE": create_scenario,
        "START": start_scenario,
        "STOP": stop_scenario,
        "UPDATE": update_scenario,
        "DELETE": delete_scenario,
    }

    methodToUse = method_switch[method]
    print(methodToUse)
    returnJSON = methodToUse(requestJSON)
    return (returnJSON)