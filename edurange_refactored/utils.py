"""Helper utilities and decorators."""
import json
import os

import csv
import re

import yaml
import markdown as md
import ast
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
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if not user.is_admin:
        abort(403)


def check_instructor():
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if not user.is_instructor:
        abort(403)


def check_privs():
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if not user.is_instructor and not user.is_admin:
        abort(403)


def check_role_view(mode):
    """Check if view mode is compatible with role (admin, instructor, student)."""
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if not user.is_admin and not user.is_instructor:
        abort(403)  # student's don't need their role checked
        return None  # a student has no applicable role. does abort stop the calling/parent function?
    else:
        mode = request.args["mode"]
        if mode not in ["studentView", "instructorView", "adminView"]:
            abort(400)  # only supported views
        elif user.is_instructor and not user.is_admin:  # instructor only
            if mode == "studentView":
                return True  # return true since viewMode should be set
            elif mode == "adminView":
                abort(403)  # instructors can't choose adminView
            else:
                return False  # return false since viewMode should be dropped
        elif user.is_admin:
            if mode in ["studentView", "instructorView"]:
                return True

            return False
        else:
            abort(403)  # who are you?!
            return None


def generateNavElements(role, view):
    """Makes decisions and calls correct generators for navigational links based on role."""
    views = None
    links = None
    if role is None: # user not logged in
        return {'views': views, 'links': links}

    if role in ['a', 'a/i', 'i']:
        viewSwitch = {
            'a': genAdminViews,     # call generator for admins view links
            'a/i': genAdminViews,   # call generator for admins view links
            'i': genInstructorViews # call generator for instructors view links
        }
        views = viewSwitch[role]() # call view link generator function based on role

    linkSwitch = {
        'a': genAdminLinks,      # call generator for admin links,
        'a/i': genAdminLinks,    # ^ pass view so function can redirect to correct link generator
        'i': genInstructorLinks, # call generator for instructor links
        's': genStudentLinks     # call generator for student links
    }
    links = linkSwitch[role](view) # call link generator function based on role

    return {
        'views': views,  # dropdown list items for view change, to render in navbar
        'links': links   # redirecting links, to render in sidebar
    }


def create_link(route, icon, text):
    """Create html element for a sidebar link (requires route, icon class (font-awesome), and text to label link)."""
    html = '''<a class="list-group-item list-group-item-action bg-secondary text-white" href="{0}">
                <i class="fa {1}" aria-hidden="true"></i>&nbsp;&nbsp;{2}
              </a>'''
    html = html.format(url_for(route), icon, text)
    return Markup(html)


def create_view(route, text):
    """Create html element for dropdown link items."""
    html = '<a class="dropdown-item" href="{0}{1}">{2}</a>'.format(url_for('dashboard.set_view'), route, text)
    return Markup(html)


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

    return None


def genInstructorLinks(view):
    """Generate links for instructors based on selected view."""
    if view == 'studentView':
        return genStudentLinks()
    elif not view:
        dashboard = create_link('dashboard.instructor', 'fa-desktop', 'Instructor Dashboard')
        scenarios = create_link('dashboard.scenarios', 'fa-align-justify', 'Scenarios')
        return [dashboard, scenarios]

    return None


def genStudentLinks(view=None): # needs common arg for switch statement
    """Generate links for students."""
    dashboard = create_link('dashboard.student', 'fa-desktop', 'Dashboard')
    return [dashboard] # return array to avoid character print in template's for loop


def checkEx(d):
    db_ses = db.session
    scenId = db_ses.query(Scenarios).get(d)
    if scenId is not None:
        return True

    return False


def checkAuth(d):
    user = User.query.filter_by(id=current_user.id).first()
    if not user.is_instructor and not user.is_admin:
        return False

    return True


def checkEnr(_id):
    enr = (
        db.session.query(GroupUsers.group_id)
                  .filter(ScenarioGroups.scenario_id == _id)
                  .filter(GroupUsers.group_id == ScenarioGroups.group_id)
                  .filter(GroupUsers.user_id == current_user.id)
                  .first()
    )

    if enr is not None:
        return True

    return False


def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""

    return value.strftime(format)


# IMPROV: write helper function to read YAML file.
def getDesc(t):
    t = t.lower().replace(" ", "_")
    with open("./scenarios/prod/{0}/{0}.yml".format(t)) as yml:
        document = yaml.full_load(yml)
        for item, doc in document.items():
            if item == "Description":
                return doc


# IMPROV: write helper function to read YAML file.
def getGuide2(t):
    t = t.lower().replace(" ", "_")
    with open("./scenarios/prod/{0}/{0}.yml".format(t)) as yml:
        document = yaml.full_load(yml)
        for item, doc in document.items():
            if item == "Codelab":
                return doc

    return "No Codelab for this Scenario"


def getGuide(scenario):
    """Return the markdown guide for the given scenario."""
    scenario = scenario.title().replace(" ", "_")
    host = os.getenv('HOST_EXTERN_ADDRESS', '127.0.0.1')
    g = host + "/tutorials/{0}/{0}.md".format(scenario)
    file = "./edurange_refactored/templates/tutorials/{0}/{0}.md".format(scenario)
    with open(file, encoding="utf-8") as fd:
        contents = fd.read()
        contents = contents.replace('127.0.0.1', host)
        return md.markdown(contents)


def getPass(scenario, username):
    """Return the username's password for the given scenario."""
    scenario = "".join(e for e in scenario if e.isalnum())
    with open('./data/tmp/{}/students.json'.format(scenario)) as fd:
        data = json.load(fd)
        password = data.get(username)[0].get('password')
        return password


# IMPROVEMENT: instead of returning a dict with index + value, return a list with the values
def getQuestions(scenario):
    c = 1
    questions = {}
    scenario = scenario.lower().replace(' ', '_')
    with open('./scenarios/prod/{}/questions.yml'.format(scenario)) as yml:
        document = yaml.full_load(yml)
        for item in document:
            questions[c] = item['Question']
            c += 1

    return questions


def tempMaker(d, i):
    db_ses = db.session
    status = db_ses.query(Scenarios.status).filter(Scenarios.id == d).first()
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
        db_ses.query(User.username).filter(Scenarios.id == d).filter(Scenarios.owner_id == User.id).first()
    )[0]

    ty = db_ses.query(Scenarios.description).filter(Scenarios.id == d).first()[0]
    scenario = db_ses.query(Scenarios.name).filter(Scenarios.id == d).first()[0]

    description = getDesc(ty)
    guide = getGuide(ty)
    questions = getQuestions(ty)

    if i == "ins":
        creationTime = db_ses.query(Scenarios.created_at).filter(Scenarios.id == d).first()[0]
        return status, ownerName, creationTime, description, ty, scenario, guide, questions
    elif i == "stu":
        user = db_ses.query(User.username).filter(User.id == current_user.id).first()[0]
        user = "".join(e for e in user if e.isalnum())
        password = getPass(scenario, user)
        return status, ownerName, description, ty, scenario, user, password, guide, questions


def responseCheck(q_number, s_id, resp, uid):
    """Read question from YAML file and check if response is correct. Return the number of points"""
    scenario_name = db.session.query(Scenarios.name).filter(Scenarios.id == s_id).first()[0]
    questions = questionReader(scenario_name)
    question = questions[q_number-1]

    if len(question['Values']) == 1:  # Only one correct answer
        answer = str(question['Values'][0]['Value'])
        if "${" in answer:
            answer = bashAnswer(s_id, uid, answer)
        if resp == answer or answer == 'ESSAY':
            return question['Points']

    elif len(question['Values']) > 1:  # Multiple correct answers
        for q in question['Values']:
            answer = q['Value']
            if "${" in answer:
                answer = bashAnswer(s_id, uid, answer)
            if resp == answer:
                return int(q['Points'])

    return 0


def bashAnswer(sid, uid, answer):
    db_ses = db.session
    username = db_ses.query(User.username).filter(User.id == uid).first()[0]
    username = "".join(e for e in username if e.isalnum())
    scenario = db_ses.query(Scenarios.name).filter(Scenarios.id == sid).first()[0]

    if "${player.login}" in answer:
        with open("./data/tmp/{}/students.json".format(scenario)) as fd:
            user = ast.literal_eval(fd.read())

        username = user[username][0]["username"]
        answerFormat = ans[0:6]
        answer = answerFormat + username
    elif "${scenario.instances" in answer:
        wordIndex = ans[21:-1].index(".")
        container = ans[21:21+wordIndex]
        with open("./data/tmp/{}/{}.tf.json".format(scenario, container)) as fd:
            content = ast.literal_eval(fd.read())

        index = content["resource"][0]["docker_container"][0][scenario + "_" + container][0]["networks_advanced"]
        for d in index:
            if d["name"] == (scenario + "_PLAYER"):
                answer = d["ipv4_address"]

    return answer


def responseQuery(uid, att, query, questions):
    tableList = []
    tmpList = []
    for entry in query:
        if entry.user_id == uid and entry.attempt == att:
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
                sR = response.student_response
                dictionary = {'number': qNum, 'question': question, 'answer': answer, 'points': points, 'student_response': sR, 'earned': r_points}
                tableList.append(dictionary)

    return tableList


def responseSelector(resp):
    query = db.session.query(Responses.id, Responses.user_id, Responses.scenario_id, Responses.attempt).all()
    for entry in query:
        if entry.id == int(resp):
            return entry


# scoring functions used in functions such as queryPolish()
# used as: scr = score(getScore(uid, att, query), questionReader(sName))
# required query entries: user_id, attempt, question, correct, student_response

'''
def getScore(usr, att, query):
    sL = []  # student response list
    for resp in query:
        if usr == resp.user_id and att == resp.attempt:
            sL.append({'question': resp.question, 'correct': resp.correct, 'response': resp.student_response})  # qnum, correct, student response
    return sL
'''


def totalScore(questions):
    """Return the total number of possible points."""
    total = 0
    for question in questions:
        total += int(question['Points'])

    return total

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


# IMPROVEMENT: simplify function (try getting rid of `i`)
# {'1': True, '2': False, ... , '6': [True, False, False, ...], '7': False}
def scoreSetup(questions):
    """Return a dict containing the question number as index and `False` as value."""
    i = 1
    checklist = {}  # list of question to be answered so duplicates are not scored
    for text in questions:
        if str(text['Type']) == 'Multi String':
            checklist[str(i)] = []
            for x in text['Values']:  # x is not used (possibly bad practice)
                checklist[str(i)].append(False)
        else:
            checklist[str(i)] = False

        i += 1

    return checklist

# if multi string, take student response into account to find the index within '6': [...] and mark true or false as normal


def scoreCheck(qnum, checkList):
    keys = list(checkList.keys())
    for k in keys:
        if k == str(qnum):
            if checkList[k]:
                return True, checkList  # answer has already been checked
            elif not checkList[k]:
                checkList[k] = True
                return False, checkList  # answer has not been checked before but is now checked
        elif str(qnum) in k and '.' in k:  # if multi string
            if checkList[k]:
                return True, checkList  # answer was already checked
            elif not checkList[k]:
                checkList[k] = True
                return False, checkList  # answer was not checked before but is now
        #elif str(qnum) in k:
            #flash("Could not check question {0} with key {1}".format(qnum, k))

    return False, checkList


def scoreCheck2(qnum, checkList, resp, quest):
    keys = list(checkList.keys())
    for k in keys:
        if k == str(qnum):
            if type(checkList[k]) == list:  # if multi string
                return False
                # check stu_resp against q.yml
                #   if stu_resp in q.yml
                #       if i in q.yml = false in checkList[k][i]
                #           return true
                #       else
            elif type(checkList[k]) == bool:    # if NOT a multi string
                if checkList[k]:
                    return True, checkList  # answer has already been checked
            elif not checkList[k]:
                checkList[k] = True
                return False, checkList  # answer has not been checked before but is now checked


# query(Responses.user_id, Responses.attempt, Responses.question, Responses.points, Responses.student_response)
# .filter(Responses.scenario_id == sid).filter(Responses.user_id == uid).filter(Responses.attempt == att).all()
#     |
#     V


def score(uid, att, query, questions):
    """Return the student's score and the total score."""
    score = 0
    checkList = scoreSetup(questions)
    for resp in query:
        if resp.user_id == uid and resp.attempt == att:  # response entry matches uid and attempt number
            if resp.points > 0:  # the student has points i.e. if the student answered correctly
                qNum = int(resp.question)
                check, checkList = scoreCheck(qNum, checkList)  # check against checkList with question number
                if not check:
                    score += resp.points

    return '{} / {}'.format(score, totalScore(questions))


def questionReader(name):
    name = "".join(e for e in name if e.isalnum())
    with open('./data/tmp/{}/questions.yml'.format(name)) as yml:
        return yaml.full_load(yml)


def queryPolish(query, sName):
    qList = []
    for entry in query:
        i = entry.id
        uid = entry.user_id
        att = entry.attempt
        usr = entry.username
        if qList is None:
            scr = score(uid, att, query, questionReader(sName))  # score(getScore(uid, att, query), questionReader(sName))
            d = {'id': i, 'user_id': uid, 'username': usr, 'score': scr, 'attempt': att}
            qList.append(d)
        else:
            error = False
            for lst in qList:
                if uid == lst['user_id'] and att == lst['attempt']:
                    error = True
                    break

            if not error:
                scr = score(uid, att, query, questionReader(sName))  # score(getScore(uid, att, query), questionReader(sName))
                d = {'id': i, 'user_id': uid, 'username': usr, 'score': scr, 'attempt': att}
                qList.append(d)

    return qList


def responseProcessing(data):
    """Response info getter."""
    db_ses = db.session
    uid = data.user_id
    username = db_ses.query(User.username).filter(User.id == uid).first()[0]

    sid = data.scenario_id
    sname = db_ses.query(Scenarios.name).filter(Scenarios.id == sid).first()[0]

    return uid, username, sid, sname, data.attempt


def setAttempt(sid):
    attempt = db.session.query(Scenarios.attempt).filter(Scenarios.id == sid).first()
    if attempt[0] == 0:
        return 1
    
    return int(attempt[0]) + 1


def getAttempt(sid):
    return db.session.query(Scenarios.attempt).filter(Scenarios.id == sid)


# IMPROVEMENT: refactor into single function with readCSV_by_name
def readCSV(id):
    arr = []
    sName = str(db.session.query(Scenarios.name).filter(Scenarios.id == id).first()[0])
    sName = "".join(e for e in sName if e.isalnum())

    file = open("./data/tmp/{0}/{0}-history.csv".format(sName))
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


def groupCSV(arr, keyIndex): # keyIndex - value in csv line to group by
    """Returns dictionary of lines with common keyIndex values."""
    dict = {}
    for entry in arr:
        key = str(entry[keyIndex].replace('-', ''))
        if key in dict:
            dict[key].append(entry)
        else:
            dict[key] = [entry]

    return dict


def getGraph(scenario, username):
    """Return SVG file for the given scenario and username."""
    try:
        with open('./data/tmp/{}/graphs/{}.svg'.format(scenario, username)) as fd:
            return fd.read()
    except:
        return None


def getLogFile(scenario):
    """Return the CSV log file's path for the given scenario."""
    logs = './data/tmp/{0}/{0}-history.csv'.format(scenario)
    if os.path.isfile(logs):
        return "." + logs

    return None


def readScenario():
    scenarios = [
        dI
        for dI in os.listdir("./scenarios/prod/")
        if os.path.isdir(os.path.join("./scenarios/prod/", dI))
    ]
    desc = []
    for s in scenarios:
        desc.append(getDesc(s))

    return 0


def recentCorrect(uid, qnum, sid):
    recent = db.session.query(Responses.points) \
        .filter(Responses.user_id == uid) \
        .filter(Responses.scenario_id == sid) \
        .filter(Responses.question == qnum) \
        .order_by(Responses.response_time.desc()).first()

    return recent

def displayCorrect(sName, uName):
    db_ses = db.session
    uid = db_ses.query(User.id).filter(User.username == uName).first()
    sid = db_ses.query(Scenarios.id).filter(Scenarios.name == sName).first()
    questions = questionReader(sName)
    ques = {}
    for i in range(1, len(questions)+1):
        rec = recentCorrect(uid, i, sid)
        if rec is not None:
            rec = rec[0]
        ques[i] = rec

    return ques


def displayProgress(sid, uid):
    att = getAttempt(sid)
    db_ses = db.session
    scenario = db_ses.query(Scenarios.name).filter(Scenarios.id == sid).first()
    query = db_ses.query(
        Responses.attempt, Responses.question, Responses.points, Responses.student_response, Responses.scenario_id, Responses.user_id
    ).filter(Responses.scenario_id == sid).filter(Responses.user_id == uid).all()
    questions = questionReader(scenario.name)
    answered, tQuest = getProgress(query, questions)
    scr, tScr = calcScr(uid, sid, att)  # score(uid, att, query, questionReader(scenario))  # score(getScore(uid, att, query), questionReader(sName))
    progress = {'questions': answered, 'total_questions': tQuest, 'score': scr, 'total_score': tScr}

    return progress


def calcScr(uid, sid, att):
    score = 0
    db_ses = db.session
    sName = db_ses.query(Scenarios.name).filter(Scenarios.id == sid).first()
    query = db_ses.query(Responses.points, Responses.question).filter(Responses.scenario_id == sid).filter(Responses.user_id == uid)\
        .filter(Responses.attempt == att).order_by(Responses.response_time.desc()).all()
    checkList = scoreSetup(questionReader(sName.name))
    for r in query:
        check, checkList = scoreCheck(r.question, checkList)
        if not check:
            score += int(r.points)
    # score = '' + str(score) + ' / ' + str(totalScore(questionReader(sName)))
    tScore = totalScore(questionReader(sName.name))
    return score, tScore


def getProgress(query, questions):
    correct = 0
    checkList = scoreSetup(questions)
    total = list(checkList.keys())[-1]
    for resp in query:
        if int(resp.points) > 0:
            q = int(resp.question)
            check, checkList = scoreCheck(q, checkList)
            if not check:
                correct += 1
    # progress = "" + str(correct) + " / " + str(total)
    return correct, total
