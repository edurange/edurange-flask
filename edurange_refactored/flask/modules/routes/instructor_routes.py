from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_user, logout_user
from edurange_refactored.user.models import User, StudentGroups, Scenarios, ScenarioGroups, GroupUsers
from edurange_refactored.extensions import db, csrf_protect
from flask import (
    Blueprint,
    request,
    jsonify,
    g
)
from edurange_refactored.flask.modules.utils.auth_utils import jwt_and_csrf_required, instructor_only
from edurange_refactored.flask.modules.utils.instructor_utils import generateTestAccts
from edurange_refactored.user.models import generate_registration_code as grc
from edurange_refactored.user.forms import changeEmailForm
from edurange_refactored.flask.modules.utils.scenario_interface import (
    list_all_scenarios, 
    scenario_create, 
    scenario_start,
    scenario_stop,
    scenario_update,
    scenario_destroy
    )
from werkzeug.exceptions import abort

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
    instructor_only()
    return jsonify ({"message":"this is /instructor_test, successful"})

@blueprint_edurange3_instructor.route("/create_group")
@jwt_and_csrf_required
def create_group():
    instructor_only()
    
    reqJSON = request.json

    group_obj = None
    code = grc()
    group_name = reqJSON['group_name']
    
    group_obj = StudentGroups.create(name=group_name, owner_id=g.current_user_id, code=code)

    # DEV_TEST
    group_obj_dict = group_obj._asdict()
    return jsonify ({"message":f"userGroup {group_name} created", 'group_obj':group_obj_dict})

@blueprint_edurange3_instructor.route("/delete_group")
@jwt_and_csrf_required
def delete_group(group_name):
    instructor_only()

    db_ses = db.session

    student_group = db_ses.query(StudentGroups).filter(StudentGroups.name == group_name).first()
    group_id = student_group.id
    group_scenarios = db_ses.query(ScenarioGroups).filter(ScenarioGroups.group_id == group_id).first()
    group_users = db_ses.query(GroupUsers).filter(GroupUsers.group_id == group_id).all()
    if group_scenarios is not None:
        jsonify({"message":"Cannot delete group - Are there still scenarios for this group?"})
    else:
        players = []
        for user in group_users:
            players.append(db_ses.query(User).filter(User.id == user.id).first())
            user.delete()
        for plr in players:
            if plr is not None:
                if plr.is_static:
                    plr.delete()
        student_group.delete()
    return jsonify({"message":"Successfully deleted group {0}".format(group_name)})


@blueprint_edurange3_instructor.route("/delete_user", methods=['POST'])
@jwt_and_csrf_required
def delete_user():
    instructor_only()

    try:
        requestJSON = request.json 
        user_to_delete = requestJSON.get('user_to_delete')

        if not user_to_delete:
            return jsonify({"message": "Missing required argument 'user_to_delete', delete aborted"}), 400

        db_ses = db.session
        user = db_ses.query(User).filter(User.name == user_to_delete).first()
        
        if not user:
            return jsonify({"message": f"Cannot delete user - does username {user_to_delete} exist?"}), 404
        else:
            db_ses.delete(user)
            db_ses.commit()
            return jsonify({"message": f"Successfully deleted user {user_to_delete}"})

    except SQLAlchemyError as e:
        db_ses.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@blueprint_edurange3_instructor.route("/generate_users")
@jwt_and_csrf_required
def generate_users():
    instructor_only()
    
    requestJSON = request.json

    generated_users = []
    generated_users = generateTestAccts(requestJSON['new_user_count'], requestJSON['group_name'])

    return jsonify (
        {
            "message" : f"{requestJSON['new_user_count']} users for group {requestJSON['group_name']} created", 
            "generated_users":generated_users
        })

@blueprint_edurange3_instructor.route("/scenario_interface", methods=["POST"])
@jwt_and_csrf_required
def scenario_interface():
    instructor_only()

    requestJSON = request.json
    if ('METHOD' not in requestJSON):
        return jsonify({'message':'method not found'}), 418

    method = requestJSON['METHOD']
    if method not in ('LIST','CREATE', 'START', 'STOP', 'UPDATE', 'DESTROY'):
        return jsonify({'message':'wrong method given'}), 418

    def list_scenarios(requestJSON):
        print("Performing LIST method")
        scenario_list = list_all_scenarios(requestJSON)
        return scenario_list

    def create_scenario(requestJSON):   
        print("Performing CREATE method")
        if ("type" not in requestJSON or "name" not in requestJSON):
            return jsonify({'message':'missing type or name arg'}), 418
        scenario_type = requestJSON["type"]
        scenario_name = requestJSON["name"]
        scenario_group_name = requestJSON["group_name"]
        scenario_users = scenario_create(scenario_type, scenario_name, scenario_group_name)
        if (scenario_users != None):
            print("CREATE method success")
            return scenario_users
        else: 
            print ("Scenario CREATE failed")
            return None


    def start_scenario(requestJSON):
        print("Performing START method")
        if ("scenario_id" not in requestJSON):
            return jsonify({'message':'missing scenario_id'}), 418
        scenario_id = requestJSON["scenario_id"]
        returnObj = scenario_start(scenario_id)
        if (returnObj != None):
            print("START method success")
            return returnObj
        else: 
            print ("Scenario START failed")
            return None
        
    def stop_scenario(requestJSON):
        print("Performing STOP method")
        if ("scenario_id" not in requestJSON):
            return jsonify({'message':'missing scenario_id'}), 418
        scenario_id = requestJSON["scenario_id"]
        returnObj = scenario_stop(scenario_id)
        if (returnObj != None):
            print("STOP method success")
            return returnObj
        else: 
            print ("Scenario STOP failed")
            return None

    def update_scenario(requestJSON):
        print("Performing UPDATE method")
        if ("scenario_id" not in requestJSON):
            return jsonify({'message':'missing scenario_id'}), 418
        scenario_id = requestJSON["scenario_id"]
        returnObj = scenario_update(scenario_id)
        if (returnObj != None):
            print("UPDATE method success")
            return returnObj
        else: 
            print ("Scenario UPDATE failed")
            return None

    def destroy_scenario(requestJSON):
        print("Performing DESTROY method")
        if ("scenario_id" not in requestJSON):
            return jsonify({'message':'missing scenario_id'}), 418
        scenario_id = requestJSON["scenario_id"]
        returnObj = scenario_destroy(scenario_id)
        if (returnObj != None):
            print("DESTROY method success")
            return returnObj
        else: 
            print ("Scenario DESTROY failed")
            return None


    def update_scenario(requestJSON):
        print("Performing UPDATE method")


    method_switch = {
        "LIST": list_scenarios,
        "CREATE": create_scenario,
        "START": start_scenario,
        "STOP": stop_scenario,
        "UPDATE": update_scenario,
        "DESTROY": destroy_scenario,
    }

    methodToUse = method_switch[method]
    returnJSON = methodToUse(requestJSON)

    return (returnJSON)