"""Helper utilities and decorators."""
import json
import os

import yaml
from flask import abort, current_app, flash, redirect, request, session, url_for
from flask_login import current_user
from flask_table import Col, Table
from jwt.jwk import OctetJWK, jwk_from_dict

from edurange_refactored.extensions import db
from .scenario_utils import item_generator

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


def check_role_view(
    mode,
):  # check if view mode compatible with role (admin/inst/student)
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


# --------


def checkEx(d):
    db_ses = db.session
    scenId = db_ses.query(Scenarios).get(d)
    if scenId is not None:
        return True
    else:
        return False


def checkAuth(d):
    db_ses = db.session
    n = current_user.id
    ownId = db_ses.query(Scenarios.owner_id).filter(Scenarios.id == d).first()
    ownId = ownId[0]
    if ownId == n:
        return True
    else:
        return False


def checkEnr(d):
    db_ses = db.session
    n = current_user.id
    enr = (
        db_ses.query(GroupUsers.group_id)
        .filter(ScenarioGroups.scenario_id == d)
        .filter(GroupUsers.group_id == ScenarioGroups.group_id)
        .filter(GroupUsers.user_id == n)
        .first()
    )
    if enr is not None:
        return True
    else:
        return False


def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)


def statReader(s):
    statSwitch = {
        0: "Stopped",
        1: "Started",
        2: "Something went very wrong",
        3: "Starting",
        4: "Stopping",
        5: "ERROR",
    }
    return statSwitch[s]


def getDesc(t):
    t = t.lower().replace(" ", "_")
    with open(
        "./scenarios/prod/" + t + "/" + t + ".yml", "r"
    ) as yml:  # edurange_refactored/scenarios/prod
        document = yaml.full_load(yml)
        for item, doc in document.items():
            if item == "Description":
                d = doc
    return d


def getGuide(t):
    #g = "No Codelab for this Scenario"
    t = t.lower().replace(" ", "_")
    with open(
        "./scenarios/prod/" + t + "/" + t + ".yml", "r"
    ) as yml:  # edurange_refactored/scenarios/prod
        document = yaml.full_load(yml)
        for item, doc in document.items():
            if item == "Codelab":
                g = doc
                #print(g)
                #return g
    #g = "No Codelab for this Scenario"
    return g


def getPass(sn, un):
    with open('./data/tmp/' + sn + '/students.json', 'r') as f:
        data = json.load(f)
        d1 = data.get(un)[0]
        p = d1.get('password')
    return p


def getQuestions(t):
    questions = []
    t = t.lower().replace(" ", "_")
    with open(
        "./scenarios/prod/" + t + "/" + "questions.yml", "r"
    ) as yml:  # edurange_refactored/scenarios/prod
        document = yaml.full_load(yml)
        for item in document:
            questions.append(item['Text'])
    return questions


def getPort(n):
    n = 0  # [WIP]
    return n


def tempMaker(d, i):
    db_ses = db.session
    # status
    stat = db_ses.query(Scenarios.status).filter(Scenarios.id == d).first()
    stat = statReader(stat[0])
    # owner name
    oName = (
        db_ses.query(User.username)
        .filter(Scenarios.id == d)
        .filter(Scenarios.owner_id == User.id)
        .first()
    )
    oName = oName[0]
    # description
    ty = db_ses.query(Scenarios.description).filter(Scenarios.id == d).first()
    ty = ty[0]
    desc = getDesc(ty)
    guide = getGuide(ty)
    questions = getQuestions(ty)
    current_app.logger.info(questions)
    # scenario name
    sNom = db_ses.query(Scenarios.name).filter(Scenarios.id == d).first()
    sNom = sNom[0]
    if i == "ins":
        # creation time
        bTime = db_ses.query(Scenarios.created_at).filter(Scenarios.id == d).first()
        bTime = bTime[0]
        return stat, oName, bTime, desc, ty, sNom, guide, questions
    elif i == "stu":
        # username
        ud = current_user.id
        usr = db_ses.query(User.username).filter(User.id == ud).first()[0]
        # password
        pw = getPass(sNom, usr)
        return stat, oName, desc, ty, sNom, usr, pw, guide, questions


# --


def responseCheck(qnum, sid, resp):
    # read correct response from yaml file
    db_ses = db.session
    s_type = db_ses.query(Scenarios.description).filter(Scenarios.id == sid).first()
    questions = questionReader(s_type[0])
    for text in questions:
        order = int(text['Order'])
        if order == qnum:
            ans = str(text['Values'][0]['Value'])
    if resp == ans:
        return True
    else:
        return False


# --


def responseQuery(uid, att, query, questions):
    tableList = []
    tmpList = []
    for entry in query:
        if entry.user_id == uid and entry.attempt == att:
            tmpList.append(entry)

    for response in tmpList:
        qNum = response.question
        for text in questions:
            order = int(text['Order'])
            if order == qNum:
                quest = text['Text']
                poi = text['Points']
                val = text['Values'][0]['Value']
                sR = response.student_response
                dictionary = {'number': qNum, 'question': quest, 'answer': val, 'points': poi, 'student_response': sR}
                tableList.append(dictionary)
    return tableList


def responseSelector(resp):
    # response selector
    db_ses = db.session
    query = db_ses.query(Responses.id, Responses.user_id, Responses.scenario_id, Responses.attempt).all()
    for entry in query:
        if entry.id == int(resp):
            data = entry
            break
    return data


def getScore(usr, att, query):
    sL = []
    for resp in query:
        if usr == resp.user_id and att == resp.attempt:
            sL.append({'question': resp.user_id, 'correct': resp.correct})
    return sL


def totalScore(questions):
    tS = 0
    for text in questions:
        tS += int(text['Points'])
    return tS


def score(scrLst, questions):
    sS = 0
    for sR in scrLst:
        if sR['correct']:
            num = int(sR['question'])
            for text in questions:
                if int(text['Order']) == num:
                    sS += int(text['Points'])
    scr = '' + str(sS) + ' / ' + str(totalScore(questions))
    return scr


def questionReader(typ):
    typ = typ.lower().replace(" ", "_")
    with open(
            "./scenarios/prod/" + typ + "/questions.yml", "r"
    ) as yml:
        document = yaml.full_load(yml)
    return document


def queryPolish(query, sType):
    qList = []
    for entry in query:
        i = entry.id
        uid = entry.user_id
        att = entry.attempt
        usr = entry.username
        if qList is None:
            scr = score(getScore(uid, att, query), questionReader(sType))
            d = {'id': i, 'user_id': uid, 'username': usr, 'score': scr, 'attempt': att}
            qList.append(d)
        else:
            error = 0
            for lst in qList:
                if uid == lst['user_id'] and att == lst['attempt']:
                    error += 1
            if error == 0:
                scr = score(getScore(uid, att, query), questionReader(sType))
                d = {'id': i, 'user_id': uid, 'username': usr, 'score': scr, 'attempt': att}
                qList.append(d)
    return qList


def responseProcessing(data):
    # response info getter
    db_ses = db.session
    # user info
    uid = data.user_id
    uname = db_ses.query(User.username).filter(User.id == uid).first()
    uname = uname[0]
    # scenario info
    sid = data.scenario_id
    sname = db_ses.query(Scenarios.name).filter(Scenarios.id == sid).first()
    sname = sname[0]
    # response info
    att = data.attempt
    return uid, uname, sid, sname, att


def getAttempt(uid, sid, qnum):
    db_ses = db.session
    query = db_ses.query(Responses.attempt).filter(Responses.user_id == uid).filter(Responses.scenario_id == sid)\
        .filter(Responses.question == qnum).first()
    if query is None:
        att = 1
    else:
        att = int(query[0]) + 1
    return att
