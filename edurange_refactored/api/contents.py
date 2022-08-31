"""Student View API routes."""
from functools import reduce
from logging import raiseExceptions
from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    session,
    jsonify,
)

import json

from sqlalchemy import func
from edurange_refactored.form_utils import process_request

from edurange_refactored.role_utils import get_roles, scenario_exists, student_has_access

from ..user.models import Responses, Scenarios

from flask_login import current_user, login_required
from jwt import JWT

from edurange_refactored.extensions import  db
from edurange_refactored.user.forms import scenarioResponseForm
from edurange_refactored.utils import TokenHelper, bashAnswer,  questionReader

blueprint = Blueprint("api", __name__, url_prefix="/api", static_folder="../static")
jwtToken = JWT()
helper = TokenHelper()
oct_data = helper.get_data()

@blueprint.route("/test", methods=["GET"])
@login_required
def test():
    """Test page."""
    srF = scenarioResponseForm()
    scenario_id = 4
    qnum = 1
    return render_template('api/test.html',
        srF=srF,
        scenario_id=scenario_id,
        qnum=qnum
    )

@blueprint.route("/get_content/<scenario_id>", methods=["GET"])
@login_required
def get_content(scenario_id):
    """
    Input:  ID number of a scenario.
    Output: The JSON outline for a student scenario. 
            This file will be located at f"data/tmp/{scenario_name_collapsed}/content.json"
    Errors: 
    TODO:   
            Instructors should only be able to access content for scenarios that they are managing.
    """
    ok, err, code = validate_usage(scenario_id)
    if ok:
        scenario_name = db.session.query(Scenarios.name)\
            .filter_by(id=scenario_id)\
            .first()\
            .name
        scenario_name = "".join(char for char in scenario_name if char.isalnum())
        with open(f"data/tmp/{scenario_name}/student_view/content.json", "r") as fp:
            content = json.load(fp)
        try:
            srF = scenarioResponseForm()
            content['StudentGuide']['csrf_token'] = srF['csrf_token']
        except KeyError as k:
            assert not current_app.config.get('WTF_CSRF_ENABLED')
        return content
    return err, code

@blueprint.route("/get_content_test/<scenario_id>", methods=["GET"])
def get_content_test(scenario_id):
    """
    Input:  ID number of a scenario.
    Output: The JSON outline for a student scenario. 
            This file will be located at f"data/tmp/{scenario_name_collapsed}/content.json"
    Errors: 
    TODO:   
            Instructors should only be able to access content for scenarios that they are managing.
    """
    with open(f"scenarios/prod/getting_started/student_view/content.json", "r") as fp:
        content = json.load(fp)
    return content


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
def get_state(scenario_id):
    """
    Input:  ID number of a scenario.
    Output: The JSON outline for a student scenario.
    Errors: 
    """
    ok, err, code = validate_usage(scenario_id)
    if ok:
        return jsonify(calc_state(current_user.id, scenario_id))
    return err, code

@blueprint.route("/get_state_test/<scenario_id>", methods=["GET"])
def get_state_test(scenario_id):
    with open(f"edurange_refactored/api/sample_state.json", "r") as fp:
        content = json.load(fp)
    return content

@blueprint.route("/post_ans/<scenario_id>", methods=["POST"])
@login_required
def post_ans(scenario_id):
    """
    Input:  ID number of a scenario.
    Effect: POST student response form data to the backend for grading.
    Errors: 
    """
    ok, err, code = validate_usage(scenario_id)
    if ok:
        ajax = process_request(request.json)
    return err, code

def validate_usage(scenario_id):
    if parsable_as(scenario_id, int):
        is_admin, is_instructor = get_roles()
        if is_admin or is_instructor or student_has_access(scenario_id):
            if scenario_exists(scenario_id):
                return True, jsonify({}), 200
            return False, jsonify({"404": "Not Found: Scenario does not exist."}), 404
        return False, jsonify({"401": "Unauthorized: You are not permitted to access this content."}), 401
    return False, jsonify({"400":"Bad Request: Required type integer"}), 400

def parsable_as(input, t: type):
    try:
        t(input)
        return True
    except Exception:
        return False


def calc_state(user_id:          int,
               scenario_id:      int):
    db_ses = db.session
    query = db_ses\
        .query(Scenarios.name, Scenarios.attempt)\
        .filter_by(id=scenario_id)\
        .first()
    scenario_name, current_attempt = query.name, query.attempt 
    query = db_ses\
        .query(Responses.points, Responses.question, Responses.student_response)\
        .filter_by(scenario_id=scenario_id)\
        .filter_by(user_id=user_id)\
        .filter_by(attempt=current_attempt)\
        .order_by(Responses.response_time.desc())\
        .all()
    # score per questions, total score so far, most recent result -- correct or incorrect
    # raise Exception(f"query {query}")
    State = {"CurrentScore" : 0}
    Questions = {}
    questions_yml = questionReader(scenario_name)
    # check for interpolations and make substitution
    for question in questions_yml:
        for ans in question["Answers"]:
            if type(ans["Value"]) == str and "${" in ans["Value"]:
                ans["Value"] = bashAnswer(scenario_id, user_id, ans["Value"])

    checkList = score_setup(questions_yml)
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
            check, checkList = score_check(row.question, row.student_response, checkList)
            # raise Exception("custom breakpoint")
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

def score_check(qNum: int, 
                response: str,
                checkList):
    """
    Description: Mark a response graded in the checklist so that the grade is computed correctly.
    Input:  Question number, 
            Student response
            Checklist object.
    Output: isChecklistUnchanged, bool
            New Checklist, object
            givePoints, bool
    """
    # resp_key = canonicalize_response(response)  
    # resp_key = canonicalize_response(
    #             scenario_id,
    #             user_id,
    #             response

    #         )
    # in case of need to canonicalize, wrap the response
    resp_key = response
    if type(checkList[qNum]) == dict: ## multi-part question
        # if all already checked or answer already in responses, 
        # don't change, don't give points
        if (checkList[qNum]["Tasks"] == 0 
                or resp_key in checkList[qNum]["Responses"]):
            return True, checkList
        else:
            checkList[qNum]["Responses"].append(resp_key)
            checkList[qNum]["Tasks"] -= 1
            return False, checkList
    else:
        if checkList[qNum]:
            return True, checkList  # answer has already been checked
        elif not checkList[qNum]:
            checkList[qNum] = True
            return False, checkList  # answer has not been checked before but is now checked



def score_setup(questions):
    checkList = {}  # List of question to be answered so duplicates are not scored.

    for index, question in enumerate(questions):
        qNum = index + 1
        if question['Type'] == "Multi String":
            checkList[qNum] = {
                "Tasks":len(question["Answers"]),
                "Responses":[]
            }
        else:
            checkList[qNum] = False

    return checkList

def is_correct(student_response: str, answer: str):
    return student_response == answer or answer == "ESSAY"

def canonicalize_response(scenario_id: int,
    user_id: int,
    student_response: str,
    answer: str):
    return student_response
