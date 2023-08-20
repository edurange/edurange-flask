



from flask_login import current_user, login_required, login_user, logout_user
from flask import (
    Blueprint,
    request,
    session,
    jsonify,
    g
)

from edurange_refactored.user.models import User,GroupUsers, ScenarioGroups, Scenarios, StudentGroups,  Responses, Notification
from edurange_refactored.extensions import db, csrf_protect
# from .auth_utils import jwt_and_csrf_required

db_ses = db.session

blueprint_routing_clone = Blueprint('public_clone', __name__) # replace "clone" with your own personal extension name, and use this extension for everything

csrf_protect.exempt(blueprint_routing_clone)


### very simple example (protected) route
@blueprint_routing_clone.route("/home_sister/dashboard/api/jwt_auth", methods=["POST"]) # DEV_ONLY
# @jwt_and_csrf_required
def jwt_auth():
    decoded = g.decoded_jwt_token   # use this to get the decoded jwt token dict/object (use g.decoded_jwt_token, not the decode() method)
    return jsonify({"message": f"Welcome {decoded['sub']}"}) # the original jwt payload is stored in the ['sub'] property...in this case, the username.

@blueprint_routing_clone.route("/home_clone/dashboard/api/sample", methods=["POST"]) # DEV_ONLY
# @jwt_and_csrf_required
def sample_route():

    requestObject = request.json
    reqSecret = requestObject["secret"]

    if reqSecret == "sesame":
        return jsonify({"message": "good job!!"})
    
    return jsonify({"message": "nope"}) # the original jwt payload is stored in the ['sub'] property...in this case, the username.
