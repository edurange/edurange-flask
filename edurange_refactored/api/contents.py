"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
)

import json

from edurange_refactored.role_utils import scenario_exists

from ..user.models import User, Scenarios

from flask_login import current_user, login_required, login_user, logout_user
from jwt import JWT
from jwt.exceptions import JWTDecodeError

from edurange_refactored.extensions import bcrypt, login_manager, db
from edurange_refactored.public.forms import (
    LoginForm,
    RequestResetPasswordForm,
    RestorePasswordForm,
)
from edurange_refactored.tasks import test_send_async_email
from edurange_refactored.user.forms import RegisterForm
from edurange_refactored.user.models import GroupUsers, StudentGroups, User
from edurange_refactored.utils import TokenHelper, flash_errors

blueprint = Blueprint("api", __name__, url_prefix="/api", static_folder="../static")
jwtToken = JWT()
helper = TokenHelper()
oct_data = helper.get_data()

@blueprint.route("/test", methods=["GET"])
def test():
    """Test page."""
    return jsonify({"test": "this is a test"})

@blueprint.route("/get_content/<scenarioId>", methods=["GET"])
@login_required
def get_content(scenarioId: int):
    """
    Input:  ID number of a scenario.
    Output: The JSON outline for a student scenario. 
            This file will be located at f"scenarios/prod/{sType}/student_view/content.json"
    Errors: 
    """
    db_ses = db.session
    if scenario := db_ses.query(Scenarios).get(scenarioId): # get scenario
        if (sType := scenario.description.lower()) in [ # in scenarios which have updated student views
            "getting_started"
        ]:
            with open(f"scenarios/prod/{sType}/student_view/content.json", "r") as fp:
                return json.load(fp)
        return jsonify({"404": "Scenario does not support this feature."})
    return jsonify({"404": "Scenario does not exist."})


@blueprint.route("/get_state/<scenarioId>", methods=["GET"])
@login_required
def get_state(scenarioId):
    """
    Input:  ID number of a scenario.
    Output: The JSON outline for a student scenario.
    Errors: 
    """
    status, owner, desc, s_type, s_name, u_name, pw, guide, questions = tempMaker(scenarioId, "stu")
    return jsonify({"TODO":"TODO"})

@blueprint.route("/post_ans/<i>", methods=["POST"])
@login_required
def post_ans(i):
    """
    Input:  ID number of a scenario.
    Output: The JSON outline for a student scenario.
    Errors: 
    """
    return jsonify({"TODO":"TODO"})
