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

from sqlalchemy import func

from edurange_refactored.role_utils import get_roles, scenario_exists, student_has_access

from ..user.models import Responses, User, Scenarios

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
from edurange_refactored.utils import TokenHelper, calcScr, displayProgress, flash_errors, getAttempt, getTotalScore, questionReader, scoreCheck, scoreSetup, tempMaker

blueprint = Blueprint("api", __name__, url_prefix="/api", static_folder="../static")
jwtToken = JWT()
helper = TokenHelper()
oct_data = helper.get_data()

@blueprint.route("/test", methods=["GET"])
def test():
    """Test page."""
    return jsonify({"test": "this is a test"})

@blueprint.route("/get_content/<scenario_id>", methods=["GET"])
@login_required
def get_content(scenario_id: int):
    """
    Input:  ID number of a scenario.
    Output: The JSON outline for a student scenario. 
            This file will be located at f"scenarios/prod/{sType}/student_view/content.json"
    Errors: 
    TODO:   
            Instructors should only be able to access content for scenarios that they are managing.
    """
    is_admin, is_instructor = get_roles()
    if is_admin or is_instructor or student_has_access(scenario_id):
        if scenario_exists(scenario_id):
            if scenario_supports(scenario_id):
                scenario_type = db.session.query(Scenarios.description)\
                    .filter_by(id=scenario_id)\
                    .first()\
                    .description\
                    .lower()
                with open(f"scenarios/prod/{scenario_type}/student_view/content.json", "r") as fp:
                    return json.load(fp)
            return jsonify({"405": "Scenario does not support this feature."}), 405
        return jsonify({"404": "Scenario does not exist."}), 404
    return jsonify({"401": "You are not permitted to access this content."}), 401


# TODO :
#       instructors can get all data associated with their students
#       admins get all 
#
"""
from the current attempt (using getAttempt)
for each question: highest score, most recent score 
"""
@blueprint.route("/get_state/<scenario_id>", methods=["GET"])
@login_required
def get_state(scenario_id: int):
    """
    Input:  ID number of a scenario.
    Output: The JSON outline for a student scenario.
    Errors: 
    """
    is_admin, is_instructor = get_roles()
    if is_admin or is_instructor or student_has_access(scenario_id):
        if scenario_exists(scenario_id):
            if scenario_supports(scenario_id):
                return jsonify(calc_state(current_user.id, scenario_id))
            return jsonify({"405": "Scenario does not support this feature."}), 405
        return jsonify({"404": "Scenario does not exist."}), 404
    return jsonify({"401": "You are not permitted to access this content."}), 401
    # return jsonify({"400": "Bad Request: Missing one of required arguments: sid, uid."}), 400

@blueprint.route("/post_ans/<i>", methods=["POST"])
@login_required
def post_ans(i):
    """
    Input:  ID number of a scenario.
    Output: The JSON outline for a student scenario.
    Errors: 
    """
    return jsonify({"TODO":"TODO"})


def calc_state(user_id:          int,
               scenario_id:      int):
    score = 0
    db_ses = db.session
    query = db_ses\
        .query(Scenarios.name, Scenarios.attempt)\
        .filter_by(id=scenario_id)\
        .first()
    scenario_name, current_attempt = query.name, query.attempt 
    query = db_ses\
        .query(Responses.points, Responses.question)\
        .filter_by(scenario_id=scenario_id)\
        .filter_by(user_id=user_id)\
        .filter_by(attempt=current_attempt)\
        .order_by(Responses.response_time.desc())\
        .all()
    # score per questions, total score so far, most recent result -- correct or incorrect
    State = {"CurrentScore" : 0}
    Questions = {}
    """
    {
        "CurrentScore" : int,
        "Questions" : {
            "1" : {
                "Score" : int,
                "Correct" : bool
            }, 
            "2" : {
                "Score" : int, 
                "Correct" : bool
            }
        }
    }
    """
    checkList = scoreSetup(questionReader(scenario_name))
    for row in query:
        # create row and set the most recent result
        points = int(row.points)
        if row.question not in Questions.keys():
            Questions[row.question] = {
                "Correct" : points > 0,
                "Score" : 0
            }
        # if the score is passing, check it off and update state
        if points > 0:
            check, checkList = scoreCheck(row.question, checkList)
            if not check:
                Questions[row.question]["Score"] += points
                State["CurrentScore"] += points

    # score = '' + str(score) + ' / ' + str(totalScore(questionReader(sName)))
    State["Questions"] = Questions
    return State

def scenario_supports(scenario_id: int):
    if scenario := db.session.query(Scenarios).get(scenario_id): # get scenario
        return scenario.description.lower() in [ # in scenarios which have updated student views
            "getting_started"
        ]