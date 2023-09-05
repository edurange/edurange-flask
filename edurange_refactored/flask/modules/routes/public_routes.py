
from flask_login import login_user, logout_user
from edurange_refactored.tasks import CreateScenarioTask
from edurange_refactored.user.models import User, StudentGroups
from edurange_refactored.extensions import db, csrf_protect
from edurange_refactored.flask.modules.utils.db_devHelper import get_instructor_data  # gets all the previous

import secrets
from edurange_refactored.flask.modules.db.schemas.ma_user import LoginSchema
from flask_jwt_simple import create_jwt

from flask import (
    Blueprint,
    request,
    session,
    jsonify,
    make_response,
    render_template
)
db_ses = db.session
edurange3_csrf = secrets.token_hex(32)


blueprint_edurange3_public = Blueprint(
    'edurange3_public', 
    __name__, 
    url_prefix='/edurange3')

# disable legacy csrf_protect; enforced w/ @jwt_and_csrf_required()
csrf_protect.exempt(blueprint_edurange3_public) 

@blueprint_edurange3_public.errorhandler(418)
def custom_error_handler(error):
    response = jsonify({"error": "request pubroute denied"})
    response.status_code = 418
    response.content_type = "application/json"
    return response

@blueprint_edurange3_public.route("/login", methods=["POST"])
def login_edurange3():
    group = "fuzz"
    g_id = db_ses.query(StudentGroups.id).filter(StudentGroups.name == group).first()
    g_id = g_id._asdict()
    CreateScenarioTask("bob", "file_wrangler", "owner", "group", g_id, "456", {"djdwn":"jnjn"})
 
    validation_schema = LoginSchema()  # instantiate validation schema
    validated_data = validation_schema.load(request.json) # validate login. reject if bad.
    
    validated_user_obj = User.query.filter_by(username=validated_data["username"]).first()
    if validated_user_obj: login_user(validated_user_obj) # login to legacy app

    if 'X-XSRF-TOKEN' not in session:
        session['X-XSRF-TOKEN'] = secrets.token_hex(32)
    
    validated_user_dump = validation_schema.dump(vars(validated_user_obj))
    del validated_user_dump['password']   # remove pw hash from return obj
    
    # - The first and only role check. [`role`] property is soon placed in jwt.
    # - Afterward, role value should be accessed from `g.current_user_role` 
    temp_role = "student"
    if validated_user_dump["is_admin"]: temp_role = "admin"
    elif validated_user_dump["is_instructor"]: temp_role = "instructor"

    json_return = { "user_data": validated_user_dump }
    # json_return["instructor_data"] = get_instructor_data() ##### DEV_ONLY

    login_return = make_response(jsonify(json_return))
    
    # generates JWT and encodes these values. (NOT hidden from user)
    # note: 'identity' is a payload keyword for Flask-JWT-Simple. best to leave it
    token_return = create_jwt(identity=({  
        "username": validated_user_dump["username"],
        "user_role": temp_role,
        "user_id": validated_user_dump["id"]
        }))
    
    # httponly=True ; mitigate XSS attacks by blinding JS to the value
    login_return.set_cookie(
        'edurange3_jwt', 
        token_return, 
        samesite='Lax', 
        httponly=True,
        path='/edurange3/'
    )
    # mitigate JWT/session related CSRF attacks
    # no httponly=True ; JS needs access to value
    login_return.set_cookie(
        'X-XSRF-TOKEN', 
        session['X-XSRF-TOKEN'], 
        samesite='Lax',
        path='/edurange3/'
)
    return login_return

# handles all other non-login requests to base URL (non-protected)
@blueprint_edurange3_public.route("/", defaults={'path': ''}, methods=["GET"])
@blueprint_edurange3_public.route("/<path:path>")
def catch_all(path):
    return render_template("public/edurange_entry.html")