"""Helper utilities and decorators."""
import json
import os

import yaml
import markdown as md
import ast
from flask import abort, flash, request, url_for
from flask_login import current_user
from jwt.jwk import OctetJWK, jwk_from_dict
from markupsafe import Markup

from edurange_refactored.extensions import db

from .user.models import Scenarios, User, Responses

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


def check_role_view(mode):  # check if view mode compatible with role (admin/inst/student)
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
            else:
                return False
        else:
            abort(403)  # who are you?!
            return None


def generateNavElements(role, view): # generate all navigational elements
    """Makes decisions and calls correct generators for navigational links based on role."""
    views, links = None, None

    if role is None: # user not logged in
        return {'views': views, 'links': links}

    if role in ['a', 'a/i', 'i']:
        viewSwitch = {
            'a': genAdminViews,   #
            'a/i': genAdminViews, # ^ call generator for admins view links
            'i': genInstructorViews # call generator for instructors view links
        }
        views = viewSwitch[role]() # call view link generator function based on role

    linkSwitch = {
        'a': genAdminLinks,    # call generator for admin links,
        'a/i': genAdminLinks,  # ^ pass view so function can redirect to correct link generator
        'i': genInstructorLinks, # call generator for instructor links
        's': genStudentLinks # call generator for student links
    }
    links = linkSwitch[role](view) # call link generator function based on role

    return {'views': views, 'links': links} # views: dropdown list items for view change, to render in navbar
                                            # links: redirecting links, to render in sidebar


def create_link(route, icon, text):
    """Create html element for a sidebar link (requires route, icon class (font-awesome), and text to label link)."""
    # html = '''<a class="list-group-item list-group-item-action bg-secondary text-white" href="{0}">
    #             <i class="fa {1}" aria-hidden="true"></i>&nbsp;&nbsp;{2}
    #           </a>'''
    html = '''<a class href="{0}">
                <i class="fa-solid {1}" aria-hidden="true"></i>&nbsp;&nbsp;{2}
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
        notification = create_link('dashboard.notification', 'fa-bell', 'Notifications')
        return [dashboard, scenarios, notification]
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


def getDescription(scenario):
    scenario = scenario.lower().replace(" ", "_")
    with open(f"./scenarios/prod/{scenario}/{scenario}.yml", "r") as yml:
        document = yaml.full_load(yml)
        for item, doc in document.items():
            if item == "Description":
                return doc


def getPass(scenario, username):
    scenario = "".join(e for e in scenario if e.isalnum())

    with open(f'./data/tmp/{scenario}/students.json') as fd:
        data = json.load(fd)

    user = data.get(username)[0]

    return user.get('password')


def getQuestions(scenario):
    scenario = scenario.lower().replace(" ", "_")

    with open(f"./scenarios/prod/{scenario}/questions.yml") as yml:
        document = yaml.full_load(yml)
        questions = {index+1: item['Text'] for index, item in enumerate(document)}

    return questions


def tempMaker(sId, i):
    db_ses = db.session
    statusSwitch = {
        0: "Stopped",
        1: "Started",
        2: "Something went very wrong",
        3: "Starting",
        4: "Stopping",
        5: "ERROR",
        7: "Building"
    }
    status = db_ses.query(Scenarios.status).filter(Scenarios.id == sId).first()
    status = statusSwitch[status[0]]

    ownerName = (
        db_ses.query(User.username).filter(Scenarios.id == sId).filter(Scenarios.owner_id == User.id).first()
    )
    ownerName = ownerName[0]

    ty = db_ses.query(Scenarios.description).filter(Scenarios.id == sId).first()
    ty = ty[0]
    description = getDescription(ty)
    guide = None #getGuide(ty)
    questions = getQuestions(ty)

    sName = db_ses.query(Scenarios.name).filter(Scenarios.id == sId).first()
    sName = sName[0]

    if i == "ins":
        createdAt = db_ses.query(Scenarios.created_at).filter(Scenarios.id == sId).first()
        createdAt = createdAt[0]

        return status, ownerName, createdAt, description, ty, sName, guide, questions
    elif i == "stu":
        username = db_ses.query(User.username).filter(User.id == current_user.id).first()[0]
        username = "".join(e for e in username if e.isalnum())
        pw = getPass(sName, username)

        return status, ownerName, description, ty, sName, username, pw, guide, questions


def checkAnswer(scenario, qnum, sid, student_answer, uid):
    """Check student answer matches correct one from YAML file."""
    questions = questionReader(scenario[0])

    question = questions[qnum-1]

    if len(question['Answers']) == 1:  # Check if there are multiple answers.
        answer = str(question['Answers'][0]['Value'])
        if "${" in answer:
            answer = bashAnswer(sid, uid, answer)
        if student_answer == answer or answer == 'ESSAY':
            return question['Points']
    else:
        correct = False
        for i in question['Answers']:
            answer = i['Value']
            if "${" in answer:
                answer = bashAnswer(sid, uid, answer)
            if student_answer == answer:
                correct = True
        if correct:
            return i['Points']

    return 0


def bashAnswer(sid, uid, ans):
    db_ses = db.session

    uName = db_ses.query(User.username).filter(User.id == uid).first()[0]
    uName = "".join(e for e in uName if e.isalnum())

    sName = db_ses.query(Scenarios.name).filter(Scenarios.id == sid).first()[0]
    sName = "".join(e for e in sName if e.isalnum())

    if "${player.login}" in ans:
        students = open(f"./data/tmp/{sName}/students.json")
        user = ast.literal_eval(students.read())
        username = user[uName][0]["username"]
        ansFormat = ans[0:6]
        newAns = ansFormat + username
        return newAns
    elif "${scenario.instances" in ans:
        wordIndex = ans[21:-1].index(".")
        containerName = ans[21:21+wordIndex]
        containerFile = open(f"./data/tmp/{sName}/{containerName}.tf.json")
        content = ast.literal_eval(containerFile.read())
        index = content["resource"][0]["docker_container"][0][sName + "_" + containerName][0]["networks_advanced"]
        ans = ""
        for d in index:
            if d["name"] == (sName + "_PLAYER"):
                ans = d["ipv4_address"]

        return ans

    return ans


def getResponses(uid, att, query, questions):
    responses = []
    entries = [entry for entry in query if entry.user_id == uid and entry.attempt == att]

    for response in entries:
        qNum = response.question
        question = questions[qNum-1]

        responses.append({
            'number': qNum,
            'question': question['Text'],
            'answer': question['Answers'][0]['Value'],
            'points': question['Points'],
            'student_response': response.student_response,
            'earned': response.points
        })

    return responses


def responseSelector(resp):
    return db.session\
            .query(Responses.id, Responses.user_id, Responses.scenario_id, Responses.attempt)\
            .filter_by(id=int(resp))\
            .first().scalar_subquery()

    # for entry in responses:
    #     if entry.id == int(resp):
    #         return entry

# scoring functions used in functions such as queryPolish()
# used as: scr = score(getScore(uid, att, query), questionReader(sName))

# required query entries: user_id, attempt, question, correct, student_response

def getTotalScore(questions):
    return sum([question['Points'] for question in questions])


def scoreSetup(questions):
    checkList = {}  # List of question to be answered so duplicates are not scored.

    for index, question in enumerate(questions):
        qNum = str(index + 1)
        if question['Type'] == "Multi String":
            checkList[qNum] = [False for _ in question['Answers']]
        else:
            checkList[qNum] = False

    return checkList


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


def getScore(uid, att, query, questions):
    stuScore = 0
    checkList = scoreSetup(questions)
    for resp in query:
        if resp.user_id == uid and resp.attempt == att:     # if response entry matches uid and attempt number
            if resp.points > 0:                             # if the student has points i.e. if the student answered correctly
                qNum = int(resp.question)
                check, checkList = scoreCheck(qNum, checkList)      # check against checkList with question number
                if not check:
                    stuScore += resp.points

    return f'{stuScore}/{getTotalScore(questions)}'


def questionReader(scenario):
    scenario = "".join(e for e in scenario if e.isalnum())

    with open(f"./data/tmp/{scenario}/questions.yml") as yml:
        return yaml.full_load(yml)


def queryPolish(query, sName):
    questions = []
    for entry in query:
        i = entry.id
        uid = entry.user_id
        att = entry.attempt
        usr = entry.username
        if questions is None:
            scr = getScore(uid, att, query, questionReader(sName))  # score(getScore(uid, att, query), questionReader(sName))
            d = {'id': i, 'user_id': uid, 'username': usr, 'score': scr, 'attempt': att}
            questions.append(d)
        else:
            error = 0
            for lst in questions:
                if uid == lst['user_id'] and att == lst['attempt']:
                    error += 1
            if error == 0:
                scr = getScore(uid, att, query, questionReader(sName))  # score(getScore(uid, att, query), questionReader(sName))
                d = {'id': i, 'user_id': uid, 'username': usr, 'score': scr, 'attempt': att}
                questions.append(d)

    return questions


def responseProcessing(data):
    '''Response info getter.'''
    db_ses = db.session

    uid, sid = data.user_id, data.scenario_id

    uname = db_ses.query(User.username).filter(User.id == uid).first()[0]
    sname = db_ses.query(Scenarios.name).filter(Scenarios.id == sid).first()[0]

    return uid, uname, sid, sname, data.attempt


def setAttempt(sid):
    currentAttempt = db.session.query(Scenarios.attempt).filter(Scenarios.id == sid).first()[0]
    if currentAttempt == 0:
        return 1

    return int(currentAttempt) + 1


def getAttempt(sid):
    return db.session.query(Scenarios.attempt).filter(Scenarios.id == sid).first()[0]


def readScenario():
    desc = []
    scenarios = [
        dI
        for dI in os.listdir("./scenarios/prod/")
        if os.path.isdir(os.path.join("./scenarios/prod/", dI))
    ]

    for scenario in scenarios:
        desc.append(getDescription(scenario))

    return 0


def recentCorrect(uid, qnum, sid):
    return db.session.query(Responses.points).filter(Responses.user_id == uid) \
        .filter(Responses.scenario_id == sid).filter(Responses.question == qnum) \
        .order_by(Responses.response_time.desc()).first()


def displayCorrectAnswers(sName, uid):
    db_ses = db.session
    
    sid = db_ses.query(Scenarios.id).filter(Scenarios.name == sName).first()[0]
    questions = questionReader(sName)
    ques = {}

    for index in range(len(questions)):
        order = index+1
        recent = recentCorrect(uid, order, sid)
        if recent is not None:
            recent = recent[0]
        else:
            recent = -1

        ques[order] = recent

    return ques


def displayProgress(sid, uid):
    db_ses = db.session
    att = getAttempt(sid)
    sName = db_ses.query(Scenarios.name).filter(Scenarios.id == sid).first()
    query = db_ses.query(Responses.attempt, Responses.question, Responses.points, Responses.student_response, Responses.scenario_id, Responses.user_id)\
        .filter(Responses.scenario_id == sid).filter(Responses.user_id == uid).all()
    questions = questionReader(sName.name)
    answered, tQuest = getProgress(query, questions)
    score, totalScore = calcScr(uid, sid, att)  # score(uid, att, query, questionReader(sName))  # score(getScore(uid, att, query), questionReader(sName))

    return {
        'questions': answered,
        'total_questions': tQuest,
        'score': score,
        'total_score': totalScore
    }


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
    tScore = getTotalScore(questionReader(sName.name))

    return score, tScore


def getProgress(query, questions):
    checkList = scoreSetup(questions)
    corr = 0
    total = list(checkList.keys())[-1]
    for resp in query:
        if int(resp.points) > 0:
            q = int(resp.question)
            check, checkList = scoreCheck(q, checkList)
            if not check:
                corr += 1

    return corr, total
