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

from .user.models import GroupUsers, ScenarioGroups, Scenarios, User

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



# Old code for tables on the dashboards (possibly not used anymore? [tbd])------


class StudentTable(Table):
    classes = ['table']
    thead_classes = ['thead-dark']
    # state = CheckCol('')
    id = Col('id')
    username = Col('username')
    email = Col('email')
    html_attrs = {
        "data-toggle": "table",
        "data-pagination": "true",
        "data-show-columns": "true",
        "data-multiple-select-row": "true",
        "data-click-to-select": "true",
        "overflow-y": "scroll",
    }  # html_attrs probably don't do anything


class Student(object):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email


class GroupTable(Table):
    classes = ["table"]
    thead_classes = ["thead-dark"]
    id = Col("id")
    name = Col("name")
    html_attrs = {
        "data-toggle": "table",
        "data-search": "true",
        "data-search-on-enter-key": "true",
        "data-show-columns": "true",
        "data-multiple-select-row": "true",
        "data-click-to-select": "true",
        "data-pagination": "true",
    }


class Group(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class GroupUserTable(Table):
    classes = ["table"]
    thead_classes = ["thead-dark"]
    id = Col("id")
    username = Col("username")
    email = Col("email")
    html_attrs = {
        "data-toggle": "table",
        "data-search": "true",
        "data-search-on-enter-key": "true",
        "data-show-columns": "true",
        "data-multiple-select-row": "true",
        "data-click-to-select": "true",
        "data-pagination": "true",
    }


class GroupUser(object):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email


class UserInfoTable(Table):
    classes = ["table"]
    thead_classes = ["thead-dark"]
    id = Col("id")
    username = Col("username")
    email = Col("email")


class UserInfo(object):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email


class ScenarioTable(Table):
    classes = ["table"]
    thead_classes = ["thead_dark"]
    id = Col("id")
    name = Col("name")
    created_at = Col("created_at")
    status = Col("status")


class Scenario(object):
    def __init__(self, id, name, created_at, status):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.status = status


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
    t = t.lower().replace(" ", "_")
    with open(
        "./scenarios/prod/" + t + "/" + t + ".yml", "r"
    ) as yml:  # edurange_refactored/scenarios/prod
        document = yaml.full_load(yml)
        for item, doc in document.items():
            if item == "Codelab":
                g = doc
                #print(g)
    return g

def getPass(sn, un):
    with open('./data/tmp/' + sn + '/students.json', 'r') as f:
        data = json.load(f)
        d1 = data.get(un)[0]
        p = d1.get('password')
    return p


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
    # scenario name
    sNom = db_ses.query(Scenarios.name).filter(Scenarios.id == d).first()
    sNom = sNom[0]
    if i == "ins":
        # creation time
        bTime = db_ses.query(Scenarios.created_at).filter(Scenarios.id == d).first()
        bTime = bTime[0]
        return stat, oName, bTime, desc, ty, sNom, guide
    elif i == "stu":
        # username
        ud = current_user.id
        usr = db_ses.query(User.username).filter(User.id == ud).first()[0]
        # password
        pw = getPass(sNom, usr)
        return stat, oName, desc, ty, sNom, usr, pw, guide


#
