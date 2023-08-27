


from flask_login import login_user, logout_user
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    jsonify,
    make_response,
    g
)
from edurange_refactored.user.models import (
    User,
    GroupUsers, 
    ScenarioGroups, 
    Scenarios, 
    StudentGroups,  
    Responses, 
    Notification
)
from ..form_utils import process_request
from ..scenario_utils import identify_state
from ..utils import (
    displayProgress,
    tempMaker,
)
from edurange_refactored.extensions import db, csrf_protect
import edurange_refactored.flask.modules.utils.db_devHelper as dbHelper

import secrets
from marshmallow import ValidationError
from edurange_refactored.flask.modules.db.schemas.ma_user import LoginSchema
from flask_jwt_simple import create_jwt
from edurange_refactored.flask.modules.utils.auth_utils import jwt_and_csrf_required
from datetime import datetime, timedelta 

db_ses = db.session
csrf_token_sister = secrets.token_hex(32)
blueprint_routing_sister = Blueprint('public_sister', __name__)
csrf_protect.exempt(blueprint_routing_sister) # disables legacy csrf_protect interference; enforced elsewhere


def convert_form_to_dict(form):
    return {field.name: field.data for field in form}


@blueprint_routing_sister.before_request
def ensure_csrf_token():
    if 'csrf_token_sister' not in session:
        session['csrf_token_sister'] = secrets.token_hex(32)


@blueprint_routing_sister.errorhandler(ValidationError)
def handle_marshmallow_error(err):
    return jsonify(err.messages), 400


@blueprint_routing_sister.route("/home_sister/login", methods=["POST"])
def login_sister():
    
    
    data = request.json

##### this manual CSRF check is needed only for login. for all other routes, use @jwt_and_csrf_required #####
    csrf_token_client = request.headers.get('X-CSRFToken')
    csrf_token_sister = session['csrf_token_sister']
    if csrf_token_client != csrf_token_sister:
        return jsonify({"error": f"invalid request (client {csrf_token_client} vs server {csrf_token_sister})"}), 400 ### DEV_ONLY 



    validation_schema = LoginSchema()  # instantiate validation schema
    validated_data = validation_schema.load(data) # runs data through validator, returns error if bad
    
    validated_user_obj = User.query.filter_by(username=validated_data["username"]).first() # retrieve schema-designated data and format it
    if validated_user_obj: login_user(validated_user_obj) # log in the user with flask_login to legacy app (log out needed)
    
    validated_user_dump = validation_schema.dump(vars(validated_user_obj)) # retrieve schema-designated data and format it
    
    
    json_return = { "user": validated_user_dump }
    json_return["instructor_data"] = dbHelper.get_instructor_data() # get full instructor data and return it #### DEV_ONLY

    final_response = make_response(jsonify(json_return))
    token_return = create_jwt(identity=validated_user_dump["username"]) # generates token and encodes the username. 
                                                                        # 'identity' is a payload keyword for Flask-JWT-Simple. best to leave it alone
    final_response.set_cookie('authorization', token_return, samesite='Lax', secure=True, httponly=True, path='/home_sister/') # sets http only cookie to user's browser
    
    return final_response


### very simple example (protected) route
@blueprint_routing_sister.route("/home_sister/dashboard/api/jwt_auth", methods=["POST"]) # DEV_ONLY
@jwt_and_csrf_required
def jwt_auth():
    decoded = g.decoded_jwt_token   # use this to get the decoded jwt token dict/object (use g.decoded_jwt_token, not the decode() method)
    return jsonify({"message": f"Welcome {decoded['sub']}"}) # the original jwt payload is stored in the ['sub'] property...in this case, the username.


@blueprint_routing_sister.route("/home_sister/", defaults={'path': ''}, methods=["GET"])
@blueprint_routing_sister.route("/home_sister/<path:path>")
def catch_all(path):
    return render_template("public/home_sister.html",csrf_token_sister=session['csrf_token_sister'])


###### Dev playground below (don't use as example) ###### 

@blueprint_routing_sister.route("/home_sister/skeletonkey", methods=['GET', 'POST']) ########## DEV_ONLY !!!
@jwt_and_csrf_required
def skeletonkey(): return jsonify( dbHelper.get_instructor_data() ) ########## DEV_ONLY !!! 


@blueprint_routing_sister.route("/home_sister/dashboard/api/get_scenario", methods=["POST"])
@jwt_and_csrf_required
def student():
    data = request.json
    thisUserID = data["userID"]

    db_ses = db.session
    currentUserId = thisUserID

    userInfoQuery = db_ses.query(User.id, User.username, User.email).filter(User.id == currentUserId).first()
    userInfo = {
        "id": userInfoQuery.id,
        "username": userInfoQuery.username,
        "email": userInfoQuery.email
    }
    
    groupsQuery = db_ses.query(StudentGroups.id, StudentGroups.name, GroupUsers) \
        .filter(GroupUsers.user_id == currentUserId) \
        .filter(GroupUsers.group_id == StudentGroups.id).all()
    groups = [{"id": group.id, "name": group.name} for group in groupsQuery]

    scenarioTableQuery = (
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
    ).all()

    scenarioTable = [
        {
            "id": scenario.id,
            "sname": scenario.sname,
            "type": scenario.type,
            "gname": scenario.gname,
            "iname": scenario.iname
        }
        for scenario in scenarioTableQuery
    ]

    return jsonify(
        userInfo=userInfo,
        groups=groups,
        scenarioTable=scenarioTable
    )


@blueprint_routing_sister.route("/home_sister/api/get_actman", methods=['POST'])
@jwt_and_csrf_required
def account():

    csrf_token_client = request.headers.get('X-CSRFToken')
    csrf_token_sister = session['csrf_token_sister']
    data = request.json
    db_ses = db.session
    userId = data["id"]

    user = db_ses.query(User).filter(User.id == userId).first()
    if csrf_token_client != csrf_token_sister:
        return jsonify({"error": f"invalid request (client {csrf_token_client} vs server {csrf_token_sister})"}), 400 ########## DEV_ONLY !!! 
        # return jsonify({"error": f"invalid request"}), 400 ######### FOR_PROD !!

    # none of this stuff should need updates
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

    return jsonify(
        groupCount=groupCount,
        label=label,
    )


@blueprint_routing_sister.route("/home_sister/dashboard/api/student_scenarios/<i>", methods=["POST"]) # DEV_ONLY
@jwt_and_csrf_required
def student_scenario(i):
    
    #     if scenario_exists(i): ## dev-disabled; probably should exist but commented for now 

    status, owner, desc, s_type, s_name, u_name, pw, guide, questions = tempMaker(i, "stu")
    # query = db_ses.query(User.id)\
    #    .filter(Responses.scenario_id == i).filter(Responses.user_id == User.id).all()
    uid = session.get("_user_id")
    # att = db_ses.query(Scenarios.attempt).filter(Scenarios.id == i).first()
    addresses = identify_state(s_name, status)
  
    # may need new validation, since we're mostly not using forms as they exist.
    ajax = process_request(request.data)  # scenarioResponseForm(request.form) # this validates it (legacy)

    if ajax:
        return jsonify( # updated to just return jsonified response, no html.  if data is embedded in html, it needs other extraction means.
            # "utils/student_answer_response.html",
            progress=displayProgress(i, uid),
            score=ajax[1]
        )

    return jsonify(i) # should never reach this line if things work right.

