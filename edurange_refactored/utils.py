"""Helper utilities and decorators."""
import ast
import csv
import json
import markdown as md
import os
import yaml

from flask import abort, flash, request, url_for
from flask_login import current_user
from jwt.jwk import OctetJWK, jwk_from_dict
from markupsafe import Markup

from edurange_refactored.extensions import db

from .user.models import GroupUsers, ScenarioGroups, Scenarios, User, Responses

path_to_key = os.path.dirname(os.path.abspath(__file__))


def load_key_data(name, mode="rb"):
    abspath = os.path.normpath(os.path.join(path_to_key, "templates/utils/.keys", name))
    with open(abspath, mode=mode) as fh:
        return fh.read()


class TokenHelper:
    def __init__(self):
        self.data = jwk_from_dict(json.loads(load_key_data("oct.json", "r")))
        self.octet_obj = OctetJWK(self.data.key, self.data.kid)

    def get_JWK(self):
        return self.octet_obj

    def get_data(self):
        return self.data

    def verify(self, token):
        self.octet_obj.verify()


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)


def check_admin():
    """Return a HTTP 403 error if the user is not an admin."""
    user = User.query.filter_by(id=current_user.id).first()
    if not user.is_admin:
        abort(403)


def check_instructor():
    """Return a HTTP 403 error if the user is not an instructor."""
    user = User.query.filter_by(id=current_user.id).first()
    if not user.is_instructor:
        abort(403)


def check_privs():
    """Return a HTTP 403 error if the user is not an instructor and not an admin."""
    if not checkAuth():
        abort(403)


def checkAuth():
    user = User.query.filter_by(id=current_user.id).first()
    if not user.is_instructor and not user.is_admin:
        return False

    return True


def check_role_view(mode):
    """Check if view mode is compatible with role (admin, instructor, student)."""
    user = User.query.filter_by(id=current_user.id).first()
    if not user.is_admin and not user.is_instructor:
        abort(403)  # No need to check students' role
    else:
        mode = request.args["mode"]
        if mode not in ["studentView", "instructorView", "adminView"]:
            abort(400)  # Only supported views
        elif user.is_instructor and not user.is_admin:  # Instructor only
            if mode == "studentView":
                return True  # Because viewMode should be set
            elif mode == "adminView":
                abort(403)  # Instructors can't choose adminView
            else:
                return False  # Because viewMode should be dropped
        elif user.is_admin:
            if mode in ["studentView", "instructorView"]:
                return True

            return False
        else:
            abort(403)


def generateNavElements(role, view):
    """Makes decisions and calls correct generators for navigational links based on role."""
    views = None
    links = None
    if role is None:  # User not logged in
        return {'views': views, 'links': links}

    if role in ['a', 'a/i', 'i']:
        viewSwitch = {
            'a': genAdminViews,      # call generator for admins view links
            'a/i': genAdminViews,    # call generator for admins view links
            'i': genInstructorViews  # call generator for instructors view links
        }
        views = viewSwitch[role]()   # call view generator function based on role

    linkSwitch = {
        'a': genAdminLinks,       # call generator for admin links
        'a/i': genAdminLinks,     # ^ pass view so function can redirect to correct link generator
        'i': genInstructorLinks,  # call generator for instructor links
        's': genStudentLinks      # call generator for student links
    }
    links = linkSwitch[role](view)  # call link generator function based on role

    return {
        'views': views,  # dropdown list items for view change, to render in navbar
        'links': links   # redirecting links, to render in sidebar
    }


def create_link(route, icon, text):
    """Create the HTML element for a sidebar link (requires route, icon class (font-awesome), and text to label link)."""
    html = \
    '''<a class="list-group-item list-group-item-action bg-secondary text-white" href="{0}">
        <i class="fa {1}" aria-hidden="true"></i>&nbsp;&nbsp;{2}
    </a>'''.format(url_for(route), icon, text)

    return Markup(html)


def create_view(route, text):
    """Create HTML element for dropdown link items."""
    return Markup(
        '<a class="dropdown-item" href="{0}{1}">{2}</a>'.format(url_for('dashboard.set_view'), route, text)
    )


def genAdminViews():
    """Generate 'select view' elements for admin users."""
    return [
        create_view('?mode=adminView', 'Admin View'),
        create_view('?mode=instructorView', 'Instructor View'),
        create_view('?mode=studentView', 'Student View')
    ]


def genInstructorViews():
    """Generate 'select view' elements for instructors."""
    return [
        create_view('?mode=instructorView', 'Instructor View'),
        create_view('?mode=studentView', 'Student View')
    ]


def genAdminLinks(view):
    """Generate links for admin users based on selected view."""
    if not view:
        dashboard = create_link('dashboard.admin', 'fa-desktop', 'Admin Dashboard')
        scenarios = create_link('dashboard.scenarios', 'fa-align-justify', 'Scenarios')
        return [dashboard, scenarios]
    elif view == 'instructorView':
        return genInstructorLinks(None)
    elif view == 'studentView':
        return genStudentLinks()


def genInstructorLinks(view):
    """Generate links for instructors based on selected view."""
    if view == 'studentView':
        return genStudentLinks()
    elif not view:
        dashboard = create_link('dashboard.instructor', 'fa-desktop', 'Instructor Dashboard')
        scenarios = create_link('dashboard.scenarios', 'fa-align-justify', 'Scenarios')
        return [dashboard, scenarios]


def genStudentLinks(view=None):
    """Generate links for students. Needs common argument for switch statement."""
    dashboard = create_link('dashboard.student', 'fa-desktop', 'Dashboard')
    return [dashboard]  # Return array to avoid character print in template's for loop


def scenarioExists(_id):
    """Return True if the scenario exists; else return False."""
    s_id = db.session.query(Scenarios).get(_id)
    return bool(s_id)


def checkEnr(_id):
    enr = db.session.query(GroupUsers.group_id) \
                    .filter(ScenarioGroups.scenario_id == _id) \
                    .filter(GroupUsers.group_id == ScenarioGroups.group_id) \
                    .filter(GroupUsers.user_id == current_user.id) \
                    .first()

    return bool(enr)


# NOTE: defined in wsgi.py and in autoapp.py; not called from here
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""

    return value.strftime(format)


def parseScenarioConfig(scenario):
    """Parse the YAML file of the given scenario."""
    scenario = scenario.lower().replace(" ", "_")
    with open("./scenarios/prod/{0}/{0}.yml".format(scenario)) as yml:
        return yaml.full_load(yml)


# NOTE: unused function
def getScenarioCodelab(scenario):
    """Get the scenario's codelab link."""
    document = parseScenarioConfig(scenario)
    for item, doc in document.items():
        if item == "Codelab":
            return doc

    return "No codelab for this scenario"


def getScenarioDescription(scenario):
    """Get the scenario's description."""
    document = parseScenarioConfig(scenario)
    for item, doc in document.items():
        if item == "Description":
            return doc


def getScenarioGraph(scenario, username):
    """Get the scenario's graph for the given username."""
    try:
        with open('./data/tmp/{}/graphs/{}.svg'.format(scenario, username)) as fd:
            return fd.read()
    except FileNotFoundError as e:
        return e


def getScenarioGuide(scenario):
    """Get the scenario's markdown guide."""
    scenario = scenario.title().replace(" ", "_")
    host = os.getenv('HOST_EXTERN_ADDRESS', '127.0.0.1')
    # g = host + "/tutorials/{0}/{0}.md".format(scenario)
    file = "./edurange_refactored/templates/tutorials/{0}/{0}.md".format(scenario)
    with open(file, encoding="utf-8") as fd:
        contents = fd.read()
        contents = contents.replace('127.0.0.1', host)
        return md.markdown(contents)


def getScenarioLogs(scenario):
    """Return the CSV log file's path for the given scenario."""
    logs = './data/tmp/{0}/{0}-history.csv'.format(scenario)
    if os.path.isfile(logs):
        return "." + logs


# IMPROV: keep code DRY, "".join(e for e in scenario if e.isalnum()) is used more times.
def getScenarioPassword(scenario, username):
    """Return the username's password for the given scenario."""
    scenario = "".join(e for e in scenario if e.isalnum())
    with open('./data/tmp/{}/students.json'.format(scenario)) as fd:
        data = json.load(fd)
        return data.get(username)[0].get('password')


# IMPROVEMENT: instead of returning a dict with index + value, return a list with the values
def getScenarioQuestions(scenario):
    c = 1
    questions = {}
    scenario = scenario.lower().replace(' ', '_')
    with open('./scenarios/prod/{}/questions.yml'.format(scenario)) as yml:
        document = yaml.full_load(yml)
        for item in document:
            questions[c] = item['Question']
            c += 1

    return questions


def getScenariosDescription():
    """Get all the scenario descriptions."""
    descriptions = []
    scenarios = [
        dI
        for dI in os.listdir("./scenarios/prod/")
        if os.path.isdir(os.path.join("./scenarios/prod/", dI))
    ]

    for scenario in scenarios:
        descriptions.append(getScenarioDescription(scenario))

# IMPROV: remove "".join(e for e in user if e.isalnum()); this is often repeated in utils.py
def makeTmpDir(s_id, mode):
    status = db.session.query(Scenarios.status).filter(Scenarios.id == s_id).first()
    status = {
        0: "Stopped",
        1: "Started",
        2: "Something went very wrong",
        3: "Starting",
        4: "Stopping",
        5: "ERROR",
        7: "Building"
    }[status[0]]

    ownerName = (
        db.session.query(User.username).filter(Scenarios.id == s_id).filter(Scenarios.owner_id == User.id).first()
    )[0]

    ty = db.session.query(Scenarios.description).filter(Scenarios.id == s_id).first()[0]
    scenario = db.session.query(Scenarios.name).filter(Scenarios.id == s_id).first()[0]

    description = getScenarioDescription(ty)
    guide = getScenarioGuide(ty)
    questions = getScenarioQuestions(ty)

    if mode == "ins":
        creationTime = db.session.query(Scenarios.created_at).filter(Scenarios.id == s_id).first()[0]
        return status, ownerName, creationTime, description, ty, scenario, guide, questions
    elif mode == "stu":
        user = db.session.query(User.username).filter(User.id == current_user.id).first()[0]
        user = "".join(e for e in user if e.isalnum())
        password = getScenarioPassword(scenario, user)
        return status, ownerName, description, ty, scenario, user, password, guide, questions


def checkStudentResponse(questionNumber, s_id, resp, uid):
    """Read question from YAML file. If response is correct, return points; else return 0."""
    scenario = db.session.query(Scenarios.name).filter(Scenarios.id == s_id).first()[0]
    questions = parseQuestions(scenario)
    question = questions[questionNumber-1]

    if question['Type'] == 'String':
        # TODO: check if only one answer is valid
        answer = str(question['Value'])  # Cast because some answers may be integers
        if "${" in answer:
            answer = parseBashAnswer(s_id, uid, answer)
        if resp == answer or \
            answer == 'ESSAY' or \
            ('Case-insesitive' in question['Options'] and resp.lower() == answer.lower()):
            # Check if response equals actual answer (whether case-sensitive or not) or if it's an essay question
            return question['Points']
    elif question['Type'] == 'Multi String':
        for answer in question['Values']:
            possibleAnswer = str(answer['Value'])
            if "${" in possibleAnswer:
                possibleAnswer = parseBashAnswer(s_id, uid, possibleAnswer)
            if resp == possibleAnswer or \
                ('Case-insesitive' in question['Options'] and resp.lower() == answer.lower()):
                # Check if response equals possible answer (whether case-sensitive or not)
                return answer['Points']

    return 0  # Unkown type of question


def parseBashAnswer(sid, uid, answer):
    username = db.session.query(User.username).filter(User.id == uid).first()[0]
    username = "".join(e for e in username if e.isalnum())

    scenario = db.session.query(Scenarios.name).filter(Scenarios.id == sid).first()[0]

    if "${player.login}" in answer:
        with open("./data/tmp/{}/students.json".format(scenario)) as fd:
            user = ast.literal_eval(fd.read())

        username = user[username][0]["username"]
        answerFormat = answer[0:6]
        answer = answerFormat + username
    elif "${scenario.instances" in answer:
        wordIndex = answer[21:-1].index(".")
        container = answer[21:21+wordIndex]
        with open("./data/tmp/{}/{}.tf.json".format(scenario, container)) as fd:
            content = ast.literal_eval(fd.read())

        index = content["resource"][0]["docker_container"][0][scenario + "_" + container][0]["networks_advanced"]
        for d in index:
            if d["name"] == (scenario + "_PLAYER"):
                answer = d["ipv4_address"]

    return answer


# WIP: YAML object structure changed.
def responseQuery(uid, attempt, query, questions):
    tableList = []
    tmpList = []
    for entry in query:
        if entry.user_id == uid and entry.attempt == attempt:
            tmpList.append(entry)

    for response in tmpList:
        qNum = response.question
        r_points = response.points
        for i in range(len(questions)):
            q = questions[i]
            if i+1 == qNum:
                question = q['Question']
                points = q['Points']
                answer = q['Values'][0]['Value']

                tableList.append({
                    'number': qNum, 'question': question, 'answer': answer, 'points': points, 'student_response': response.student_response, 'earned': r_points
                })

    return tableList


def responseSelector(resp):
    query = db.session.query(Responses.id, Responses.user_id, Responses.scenario_id, Responses.attempt).all()
    for entry in query:
        if entry.id == int(resp):
            return entry


# Scoring functions used in functions such as queryPolish()
# used as: scr = score(getScore(uid, attempt, query), parseQuestions(sName))
# required query entries: user_id, attempt, question, correct, student_response

def totalScore(questions):
    """Return the total number of possible points."""
    return sum(question['Points'] for question in questions)

'''
def score(scrLst, questions):
    sS = 0  # student score
    checkList = scoreSetup(questions)  # questions scored checklist
    for sR in scrLst:  # response in list of student responses
        if sR['correct']:
            num = int(sR['question'])  # question number
            for text in questions:
                if int(text['Order']) == num:
                    check, checkList = scoreCheck(num, checkList)
                    if not check:
                        if str(text['Type']) == "Multi String":
                            for i in text['Values']:
                                if i['Value'] == sR['response']:
                                    sS += int(text['Values'][i]['Points'])
                        else:
                            sS += int(text['Points'])
    scr = '' + str(sS) + ' / ' + str(totalScore(questions))
    return scr
'''


# IMPROVEMENT: simplify function by getting rid of `i`
# {'1': True, '2': False, ... , '6': [True, False, False, ...], '7': False}
def scoreSetup(questions):
    """Return a dict containing the question number as index and `False` as value."""
    i = 1
    checklist = {}  # List of question to be answered so duplicates are not scored
    for question in questions:
        # take student response into account to find the index within '6': [...] and mark true or false as normal
        if str(question['Type']) == 'Multi String':
            checklist[str(i)] = []
            for x in question['Values']:  # x is not used (possibly bad practice)
                checklist[str(i)].append(False)
        else:
            checklist[str(i)] = False

        i += 1

    return checklist


# TODO: review function, nested if's perform the same operations
def scoreCheck(qnum, checkList):
    keys = list(checkList.keys())
    for k in keys:
        if k == str(qnum):
            if checkList[k]:  # Answer has already been checked
                return True, checkList
            elif not checkList[k]:  # Answer has not been checked before but is now
                checkList[k] = True
                return False, checkList
        elif str(qnum) in k and '.' in k:  # Multi string
            if checkList[k]:
                return True, checkList
            elif not checkList[k]:
                checkList[k] = True
                return False, checkList
        #elif str(qnum) in k:
            #flash("Could not check question {0} with key {1}".format(qnum, k))

    return False, checkList


def scoreCheck2(qnum, checkList, resp, quest):
    keys = list(checkList.keys())
    for k in keys:
        if k == str(qnum):
            if type(checkList[k]) == list:  # multi string
                return False
                # check stu_resp against q.yml
                #   if stu_resp in q.yml
                #       if i in q.yml = false in checkList[k][i]
                #           return true
            elif type(checkList[k]) == bool:  # NOT a multi string
                if checkList[k]:
                    return True, checkList  # answer has already been checked
            elif not checkList[k]:
                checkList[k] = True
                return False, checkList  # answer has not been checked before but is now checked


# query(Responses.user_id, Responses.attempt, Responses.question, Responses.points, Responses.student_response)
# .filter(Responses.scenario_id == sid).filter(Responses.user_id == uid).filter(Responses.attempt == att).all()
def getScore(uid, attempt, query, questions):
    """Return the student's score and the total score."""
    score = 0
    checkList = scoreSetup(questions)
    for resp in query:
        if resp.user_id == uid and resp.attempt == attempt:  # response entry matches uid and attempt number
            if resp.points > 0:  # the student has points, i.e. if the student answered correctly
                qNum = int(resp.question)
                check, checkList = scoreCheck(qNum, checkList)  # check against checkList with question number
                if not check:
                    score += resp.points

    return '{} / {}'.format(score, totalScore(questions))


def parseQuestions(scenario):
    """Return the object of the scenario's questions."""
    scenario = "".join(e for e in scenario if e.isalnum())
    with open('./data/tmp/{}/questions.yml'.format(scenario)) as yml:
        return yaml.full_load(yml)


def queryPolish(query, scenario):
    qList = []
    for entry in query:
        _id = entry.id
        uid = entry.user_id
        attempt = entry.attempt
        username = entry.username
        if qList is None:
            score = getScore(uid, attempt, query, parseQuestions(scenario))
            qList.append({
                'id': _id, 'user_id': uid, 'username': username, 'score': score, 'attempt': attempt
            })
        else:
            for lst in qList:
                if uid == lst['user_id'] and attempt == lst['attempt']:
                    return qList

            score = getScore(uid, attempt, query, parseQuestions(scenario))
            qList.append({
                'id': _id, 'user_id': uid, 'username': username, 'score': score, 'attempt': attempt
            })

    return qList


def responseProcessing(data):
    """Response info getter."""
    uid = data.user_id
    username = db.session.query(User.username).filter(User.id == uid).first()[0]

    sid = data.scenario_id
    scenario = db.session.query(Scenarios.name).filter(Scenarios.id == sid).first()[0]

    return uid, username, sid, scenario, data.attempt


def setAttempt(sid):
    """Set or increment the scenario's attempts."""
    attempt = db.session.query(Scenarios.attempt).filter(Scenarios.id == sid).first()
    if attempt[0] == 0:
        return 1

    return int(attempt[0]) + 1


def getAttempt(sid):
    """Get the scenario's attempts."""
    return db.session.query(Scenarios.attempt).filter(Scenarios.id == sid)


def CSVHelper():
    arr = []
    scenario = db.session.query(Scenarios.name).filter(Scenarios.id == id).first()[0]
    scenario = "".join(e for e in scenario if e.isalnum())
    file = open("./data/tmp/{0}/{0}-history.csv".format(scenario))
    reader = csv.reader(file, delimiter="|", quotechar="%", quoting=csv.QUOTE_MINIMAL)

    for row in reader:
        if len(row) == 8:
            arr.append(row)

    return arr

# IMPROVEMENT: refactor into single function with readCSV_by_name
def readCSV(_id):
    arr = []
    scenario = db.session.query(Scenarios.name).filter(Scenarios.id == _id).first()[0]
    scenario = "".join(e for e in scenario if e.isalnum())

    file = open("./data/tmp/{0}/{0}-history.csv".format(scenario))
    reader = csv.reader(file, delimiter="|", quotechar="%", quoting=csv.QUOTE_MINIMAL)

    for row in reader:
        if len(row) == 8:
            arr.append(row)

    return arr


# IMPROVEMENT: refactor into single function with readCSV
def readCSV_by_name(name):
    arr = []
    file = open("./data/tmp/{0}/{0}-history.csv".format(name))
    reader = csv.reader(file, delimiter="|", quotechar="%", quoting=csv.QUOTE_MINIMAL)

    for row in reader:
        if len(row) == 8:
            arr.append(row)

    return arr


def formatCSV(arr):
    arr = []
    for entry in arr:
        tmpArr = entry.replace("#%#", "\n").replace("%", "").split("\t")
        tmpArr[6] = tmpArr[6].replace("@", "") # remove '@' from end of username
        arr.append(tmpArr)

    return arr


def groupCSV(arr, keyIndex):
    """Returns a dictionary of lines with common keyIndex values (CSV line to group by)."""
    dictionary = {}

    for entry in arr:
        key = str(entry[keyIndex].replace('-', ''))
        if key in dictionary:
            dictionary[key].append(entry)
        else:
            dictionary[key] = [entry]

    return dictionary


def getRecentCorrect(uid, qNum, sid):
    """Return the scenario's recent correct answers of the given question."""
    return db.session.query(Responses.points) \
        .filter(Responses.user_id == uid) \
        .filter(Responses.scenario_id == sid) \
        .filter(Responses.question == qNum) \
        .order_by(Responses.response_time.desc()).first()


def displayCorrect(sName, uName):
    uid = db.session.query(User.id).filter(User.username == uName).first()
    sid = db.session.query(Scenarios.id).filter(Scenarios.name == sName).first()

    _questions = {}
    questions = parseQuestions(sName)
    for qNum in range(1, len(questions)+1):
        recent = getRecentCorrect(uid, qNum, sid)
        if recent:
            recent = recent[0]
        _questions[qNum] = recent

    return _questions


def getProgress(query, questions):
    """Return the number of correct and total questions.""" 
    correct = 0
    checkList = scoreSetup(questions)
    total = list(checkList.keys())[-1]
    for resp in query:
        if int(resp.points) > 0:
            questionNumber = int(resp.question)
            check, checkList = scoreCheck(questionNumber, checkList)
            if not check:
                correct += 1

    return correct, total   # alternative: str(correct) + " / " + str(total)


def displayProgress(sid, uid):
    """Return answered questions, all questions, score, and total score."""
    attempt = getAttempt(sid)
    scenario = db.session.query(Scenarios.name).filter(Scenarios.id == sid).first()
    query = db.session.query(
        Responses.attempt, Responses.question, Responses.points, Responses.student_response, Responses.scenario_id, Responses.user_id
    ).filter(Responses.scenario_id == sid).filter(Responses.user_id == uid).all()
    questions = parseQuestions(scenario.name)
    answered, totalQuestions = getProgress(query, questions)
    score, totalScore = calculateScore(uid, sid, attempt)

    return {
        'questions': answered, 'total_questions': totalQuestions, 'score': score, 'total_score': totalScore
    }


def calculateScore(uid, sid, attempt):
    score = 0
    scenario = db.session.query(Scenarios.name).filter(Scenarios.id == sid).first()
    query = db.session.query(Responses.points, Responses.question) \
                      .filter(Responses.scenario_id == sid) \
                      .filter(Responses.user_id == uid) \
                      .filter(Responses.attempt == attempt) \
                      .order_by(Responses.response_time.desc()).all()
    checkList = scoreSetup(parseQuestions(scenario.name))
    for r in query:
        check, checkList = scoreCheck(r.question, checkList)
        if not check:
            score += int(r.points)
    # score = '' + str(score) + ' / ' + str(totalScore(parseQuestions(scenario)))
    totalScore = totalScore(parseQuestions(scenario.name))

    return score, totalScore
