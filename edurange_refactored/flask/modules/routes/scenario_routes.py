"""Student View API routes."""

from edurange_refactored.extensions import db, csrf_protect
from edurange_refactored.flask.modules.utils.db_devHelper import (
    get_user,
    get_users,
    get_groups,
    get_group_users,
    get_scenarios,
    get_scenario_groups,
    get_student_responses,
    get_instructor_data,  # gets all the previous
)
from edurange_refactored.user.models import (
    GroupUsers, 
    ScenarioGroups, 
    Scenarios, 
    Responses, 
    User,
    StudentGroups,  
)
import json
from random import seed, shuffle
from edurange_refactored.form_utils import process_request
from edurange_refactored.utils import bashAnswer,  questionReader
from edurange_refactored.role_utils import get_roles, scenario_exists, student_has_access
from edurange_refactored.user.forms import scenarioResponseForm
from flask import (
    Blueprint,
    request,
    session,
    jsonify,
    make_response,
    render_template,
    current_app,
    g, ## see note
)
from ..utils.auth_utils import jwt_and_csrf_required
from ..utils.guide_utils import (
    getContent, 
    getResponses
    )


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
blueprint_edurange3_scenarios = Blueprint('edurange3_scenario', __name__, url_prefix='/edurange3/api')
csrf_protect.exempt(blueprint_edurange3_scenarios) # enforced elsewhere

@blueprint_edurange3_scenarios.errorhandler(418)
def custom_error_handler(error):
    response = jsonify({"error": "request denied"})
    response.status_code = 418
    response.content_type = "application/json"
    return response



### Reviewed / Working Routes  ##############

@blueprint_edurange3_scenarios.route('/get_content/<int:i>', methods=['GET']) # WIP
@jwt_and_csrf_required
def get_content(i):
    current_username = g.current_username
    current_scenario_id = i
    if (
        not isinstance(i, int)
        or i < 0 
        or i > 99
        ):
            return jsonify({'error': 'invalid scenario ID'}), 418 # DEV_ONLY (replace with standard denial msg)

    contentJSON, credentialsJSON, unique_name = getContent(current_scenario_id, current_username)
    # returns instructor-chosen scenario name if check good
    # you can use the name for content.json retrieval, etc
    # this is useful for reducing need for stateful user-scenario data
    # user_creds = credentialsJSON[str(current_username)]
    return jsonify({
        "contentJSON":contentJSON, 
        "credentialsJSON":credentialsJSON,
        "unique_scenario_name":unique_name
        })
    if not content.user_creds:
        return jsonify({"error": f"scenario with id {i} is found, build failed"}), 418 # DEV_ONLY
    return jsonify ({"content": content["content"], "user_creds": content["user_creds"]}), 200

@blueprint_edurange3_scenarios.route('/get_scenarios', methods=['GET'])
@jwt_and_csrf_required
def student():
    current_username = g.current_username
    current_user_id = g.current_user_id
    current_user_role = g.current_user_role
    db_ses = db.session
 
    userInfo = {
        'id': current_user_id,
        'username': current_username,
    }
    
    groupsQuery = db_ses.query(StudentGroups.id, StudentGroups.name, GroupUsers) \
        .filter(GroupUsers.user_id == current_user_id) \
        .filter(GroupUsers.group_id == StudentGroups.id).all()
    groups = [{'id': group.id, 'name': group.name} for group in groupsQuery]

    scenarioTableQuery = (
        db_ses.query(
            Scenarios.id,
            Scenarios.name.label('sname'),
            Scenarios.description.label('type'),
            StudentGroups.name.label('gname'),
            User.username.label('iname'),
        )
        .filter(GroupUsers.user_id == current_user_id)
        .filter(StudentGroups.id == GroupUsers.group_id)
        .filter(User.id == StudentGroups.owner_id)
        .filter(ScenarioGroups.group_id == StudentGroups.id)
        .filter(Scenarios.id == ScenarioGroups.scenario_id)
    ).all()

    scenarioTable = [
        {
            'scenario_id': scenario.id,
            'scenario_name': scenario.sname,
            'scenario_type': scenario.type,
            'group_name': scenario.gname,
            'owner_name': scenario.iname
        }
        for scenario in scenarioTableQuery
    ]

    return jsonify (
        userInfo=userInfo,
        groups=groups,
        scenarioTable=scenarioTable
    )



















### UNReviewed Routes Below ##############

# @blueprint_edurange3_scenarios.route('/test', methods=['GET'])
# @jwt_and_csrf_required
# def test():
#     '''Test page.'''
#     srF = scenarioResponseForm()
#     scenario_id = 4
#     qnum = 1
#     return render_template('api/test.html',
#         srF=srF,
#         scenario_id=scenario_id,
#         qnum=qnum
#     )

# @blueprint_edurange3_scenarios.route('/get_content/<scenario_id>', methods=['GET'])
# @jwt_and_csrf_required
# def get_content(scenario_id):


#     '''
#     Input:  ID number of a scenario.
#     Output: The JSON outline for a student scenario. 
#             This file will be located at f'data/tmp/{scenario_name_collapsed}/content.json'
#     Errors: 
#     TODO:   
#             Instructors should only be able to access content for scenarios that they are managing.
#     '''
#     ok, err, code = validate_usage(scenario_id)
#     if ok:
#         scenario_name = db.session.query(Scenarios.name)\
#             .filter_by(id=scenario_id)\
#             .first()\
#             .name
#         scenario_name = "".join(char for char in scenario_name if char.isalnum())
#         with open(f'data/tmp/{scenario_name}/student_view/content.json', 'r') as fp:
#             content = json.load(fp)
#         try:
#             srF = scenarioResponseForm()
#             content['StudentGuide']['csrf_token'] = srF['csrf_token']
#         except KeyError as k:
#             assert not current_app.config.get('WTF_CSRF_ENABLED')
#         return content
#     return err, code

# @blueprint_edurange3_scenarios.route('/get_content_test/<scenario_id>', methods=['GET'])
# @jwt_and_csrf_required
# def get_content_test(scenario_id):
#     """
#     Input:  ID number of a scenario.
#     Output: The JSON outline for a student scenario. 
#             This file will be located at f'data/tmp/{scenario_name_collapsed}/content.json'
#     Errors: 
#     TODO:   
#             Instructors should only be able to access content for scenarios that they are managing.
#     """
#     with open(f'scenarios/prod/getting_started/student_view/content.json', 'r') as fp:
#         content = json.load(fp)
#     return content


# # TODO :
# #       instructors can get all data associated with their students
# #       admins get all 
# #
# """
# from the current attempt (using getAttempt)
# for each question: highest score, most recent score 
# """
# @blueprint_edurange3_scenarios.route('/get_state/<scenario_id>', methods=['GET'])
# @jwt_and_csrf_required
# def get_state(scenario_id):
#     """
#     Input:  ID number of a scenario.
#     Output: The JSON outline for a student scenario.
#     Errors: 
#     """
#     ok, err, code = validate_usage(scenario_id)
#     if ok:
#         return jsonify(calc_state(current_user.id, scenario_id))
#     return err, code

# @blueprint_edurange3_scenarios.route('/get_state_test/<scenario_id>', methods=['GET'])
# @jwt_and_csrf_required
# def get_state_test(scenario_id):
#     with open(f'edurange_refactored/api/sample_state.json', 'r') as fp:
#         content = json.load(fp)
#     return content

# @blueprint_edurange3_scenarios.route('/post_ans/<scenario_id>', methods=['POST'])
# @jwt_and_csrf_required
# def post_ans(scenario_id):
#     """
#     Input:  ID number of a scenario.
#     Effect: POST student response form data to the backend for grading.
#     Errors: 
#     """
#     ok, err, code = validate_usage(scenario_id)
#     if ok:
#         ajax = process_request(request.json)
#     return err, code

# def validate_usage(scenario_id):
#     if parsable_as(scenario_id, int):
#         is_admin, is_instructor = get_roles()
#         if is_admin or is_instructor or student_has_access(scenario_id):
#             if scenario_exists(scenario_id):
#                 return True, jsonify({}), 200
#             return False, jsonify({'404': 'Not Found: Scenario does not exist.'}), 404
#         return False, jsonify({'401': 'Unauthorized: You are not permitted to access this content.'}), 401
#     return False, jsonify({'400':'Bad Request: Required type integer'}), 400

# def parsable_as(input, t: type):
#     try:
#         t(input)
#         return True
#     except Exception:
#         return False


# def calc_state(user_id:          int,
#                scenario_id:      int):
#     db_ses = db.session
#     query = db_ses\
#         .query(Scenarios.name, Scenarios.attempt)\
#         .filter_by(id=scenario_id)\
#         .first()
#     scenario_name, current_attempt = query.name, query.attempt 
#     query = db_ses\
#         .query(Responses.points, Responses.question, Responses.student_response)\
#         .filter_by(scenario_id=scenario_id)\
#         .filter_by(user_id=user_id)\
#         .filter_by(attempt=current_attempt)\
#         .order_by(Responses.response_time.desc())\
#         .all()
#     # score per questions, total score so far, most recent result -- correct or incorrect
#     # raise Exception(f'query {query}')
#     State = {'CurrentScore' : 0}
#     Questions = {}
#     questions_yml = questionReader(scenario_name)
#     # check for interpolations and make substitution
#     for question in questions_yml:
#         for ans in question['Answers']:
#             if type(ans['Value']) == str and '${' in ans['Value']:
#                 ans['Value'] = bashAnswer(scenario_id, user_id, ans['Value'])

#     checkList = score_setup(questions_yml)
#     for row in query:
#         # create row and set the most recent result
#         points = int(row.points)
#         if row.question not in Questions.keys():
#             Questions[row.question] = {
#                 'Correct' : points > 0,
#                 'Score' : 0
#             }
#         # if the score is passing, check it off and update state
#         if points > 0:
#             check, checkList = score_check(row.question, row.student_response, checkList)
#             # raise Exception('custom breakpoint')
#             if not check:
#                 Questions[row.question]['Score'] += points
#                 State['CurrentScore'] += points

#     # score = '' + str(score) + ' / ' + str(totalScore(questionReader(sName)))
#     State['Questions'] = Questions
#     return State

# def scenario_supports(scenario_id: int):
#     if scenario := db.session.query(Scenarios).get(scenario_id): # get scenario
#         return scenario.description.lower() in [ # in scenarios which have updated student views
#             'getting_started'
#         ]

# def score_check(qNum: int, 
#                 response: str,
#                 checkList):
#     """
#     Description: Mark a response graded in the checklist so that the grade is computed correctly.
#     Input:  Question number, 
#             Student response
#             Checklist object.
#     Output: isChecklistUnchanged, bool
#             New Checklist, object
#             givePoints, bool
#     """
#     # resp_key = canonicalize_response(response)  
#     # resp_key = canonicalize_response(
#     #             scenario_id,
#     #             user_id,
#     #             response

#     #         )
#     # in case of need to canonicalize, wrap the response
#     resp_key = response
#     if type(checkList[qNum]) == dict: ## multi-part question
#         # if all already checked or answer already in responses, 
#         # don't change, don't give points
#         if (checkList[qNum]['Tasks'] == 0 
#                 or resp_key in checkList[qNum]['Responses']):
#             return True, checkList
#         else:
#             checkList[qNum]['Responses'].append(resp_key)
#             checkList[qNum]['Tasks'] -= 1
#             return False, checkList
#     else:
#         if checkList[qNum]:
#             return True, checkList  # answer has already been checked
#         elif not checkList[qNum]:
#             checkList[qNum] = True
#             return False, checkList  # answer has not been checked before but is now checked



# def score_setup(questions):
#     checkList = {}  # List of question to be answered so duplicates are not scored.

#     for index, question in enumerate(questions):
#         qNum = index + 1
#         if question['Type'] == 'Multi String':
#             checkList[qNum] = {
#                 'Tasks':len(question['Answers']),
#                 'Responses':[]
#             }
#         else:
#             checkList[qNum] = False

#     return checkList

# def is_correct(student_response: str, answer: str):
#     return student_response == answer or answer == 'ESSAY'

# def canonicalize_response(scenario_id: int,
#     user_id: int,
#     student_response: str,
#     answer: str):
#     return student_response

# @blueprint_edurange3_scenarios.route('/chat_init/<scenario_id>', methods=['GET'])
# @jwt_and_csrf_required
# def gen_chat_names(scenario_id): 
#     """
#     Synopsis
#     --------
#     Return a mapping of student IDs to temporary anonymous chat usernames.
#     One name is created as <adjective><Noun> in camel case. Assumes the number of 

#     Parameters
#     ----------
#     sid : int
#         Scenario id

#     Returns
#     -------
#     dict
#         Dictionary of {student ID : chatname} mappings
    
#     """
#     # Save the db session as a variable
#     session = db.session

#     nouns = [
#             'Animal',      'Horse',     'Parrot',   'Rainbow',    'Lizard',
#             'Ghost',       'Oyster',    'Potato',   'Fish',       'Lion',
#             'Kangaroo',    'Rocket',    'Engine',   'Magician',   'Tractor',
#             'Poetry',      'Piano',     'Finger',   'Ambassador', 'Boxer',
#             'Goldsmith',   'Scavenger', 'Surgeon',  'Chemist',    'Cobra',
#             'Elk',         'Wolf',      'Tiger',    'Shark',      'Otter',
#             'Fox',         'Falcon',    'Badger',   'Bear',       'Raven',
#             'Rabbit',      'Hare',      'Ant',      'Scorpion',   'Owl',
#             'Finch',       'Starling',  'Sparrow',  'Bulldozer',  'Astronomer',
#             'Philosopher', 'Engineer',  'Catfish',  'Pirate',     'Bilder',
#             'Captain',     'Sailor',    'Cactus',   'Genie',      'Chimera',
#             'Banshee',     'Dragon',    'Pheonix',  'Basilisk',   'Griffin',
#             'Centaur',     'Sprite',    'Golem',    'Sphinx',     'Moose',
#             'Mongoose',    'Star',      'Starfish', 'Comet',      'Argonaut'
#         ]

#     adjectives = [
#         'blue',          'fast',       'squirrely',     'round',
#         'extravagant',   'orange',     'red',           'small',
#         'rotund',        'supreme',    'inconspicuous', 'fancy',
#         'enraging',      'unseen',     'proper',        'green',
#         'fabulous',      'nostalgic',  'shy',           'large',
#         'oblivious',     'obvious',    'extreme',       'unphased',
#         'frightening',   'suspicious', 'miniscule',     'enormous',
#         'gigantic',      'pink',       'fuzzy',         'sleek',
#         'fantastic',     'boring',     'colorful',      'loud',
#         'quiet',         'powerful',   'focused',       'confusing',
#         'skillful',      'purple',     'invisible',     'undecided',
#         'calming',       'tall',       'flat',          'octagonal',
#         'hexagonal',     'triangular', 'robust',        'thorough',
#         'surprising',    'unexpected', 'whimsical',     'musical',
#         'imaginary',     'squishy',    'intricate',     'complex',
#         'uncomplicated', 'efficient',  'hidden',        'sophisticated',
#         'ridiculous',    'strong',     'turquoise',     'plentiful',
#         'yodeling',      'sneaky'
#     ]

#     num_words = min(len(nouns), len(adjectives))

#     # Shuffle the lists, seeded on the scenario id
#     seed(scenario_id)
#     shuffle(nouns)
#     shuffle(adjectives)

#     # Get group id from scenario id
#     gid = session\
#                     .query(ScenarioGroups.group_id)\
#                     .filter(ScenarioGroups.scenario_id == scenario_id)\
#                     .first()[0]
#     # Get list of student ids from group id
#     student_ids = session\
#                     .query(GroupUsers.id)\
#                     .filter(GroupUsers.group_id == gid)\
#                     .all()

#     # Collect only the useful part of the DB query
#     # Reduce the ids by the number of words to allow indexing
#     student_ids = map(lambda row: row[0] % num_words, student_ids)
     
#     ok, err, code = validate_usage(scenario_id)
#     if ok:
#         return jsonify({id: adjectives[id] + nouns[id] for id in student_ids})
#     return err, code

