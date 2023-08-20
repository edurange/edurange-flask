
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
blueprint_edurange3_public = Blueprint('edurange3_public', __name__)
csrf_protect.exempt(blueprint_edurange3_public) # disables legacy csrf_protect interference; enforced elsewhere

def convert_form_to_dict(form):
    return {field.name: field.data for field in form}

@blueprint_edurange3_public.before_request
def ensure_csrf_token():
    if 'edurange3_csrf' not in session:
        session['edurange3_csrf'] = secrets.token_hex(32)


@blueprint_edurange3_public.errorhandler(ValidationError)
def handle_marshmallow_error(err):
    return jsonify(err.messages), 400


@blueprint_edurange3_public.route("/edurange3/login", methods=["POST"])
def login_edurange3():
    
    data = request.json
    csrf_token_client = request.headers.get('X-CSRFToken')
    edurange3_csrf = session['edurange3_csrf']
    if csrf_token_client != edurange3_csrf:
        return jsonify({"error": f"invalid request (client {csrf_token_client} vs server {edurange3_csrf})"}), 400 ### DEV_ONLY 

    validation_schema = LoginSchema()  # instantiate validation schema
    validated_data = validation_schema.load(data) # runs data through validator, returns error if bad
    
    validated_user_obj = User.query.filter_by(username=validated_data["username"]).first() # retrieve schema-designated data and format it
    if validated_user_obj: login_user(validated_user_obj) # log in the user with flask_login to legacy app (log out needed)
    
    validated_user_dump = validation_schema.dump(vars(validated_user_obj)) # retrieve schema-designated data and format it
    
    
    json_return = { "user": validated_user_dump }
    json_return["instructor_data"] = get_instructor_data() # get full instructor data and return it #### DEV_ONLY

    final_response = make_response(jsonify(json_return))
    token_return = create_jwt(identity=validated_user_dump["username"]) # generates token and encodes the username. 
                                                                        # 'identity' is a payload keyword for Flask-JWT-Simple. best to leave it alone
    final_response.set_cookie('edurange3_jwt', token_return, samesite='Lax', secure=True, httponly=True, path='/edurange3/') # sets http only cookie to user's browser
    
    return final_response

@blueprint_edurange3_public.route("/edurange3/", defaults={'path': ''}, methods=["GET"])
@blueprint_edurange3_public.route("/edurange3/<path:path>")
def catch_all(path):
    return render_template("public/edurange3_home.html",edurange3_csrf=session['edurange3_csrf'])


