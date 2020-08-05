"""Helper utilities and decorators."""
from flask import flash, abort, request, session, redirect, url_for, current_app, Markup
from flask_login import current_user
from flask_table import Table, Col
from jwt.jwk import jwk_from_dict, OctetJWK

from .user.models import User, Scenarios, ScenarioGroups, GroupUsers
from edurange_refactored.extensions import db

import yaml
import json
import os

path_to_key = os.path.dirname(os.path.abspath(__file__))


def load_key_data(name, mode='rb'):
    abspath = os.path.normpath(os.path.join(path_to_key, 'templates/utils/.keys', name))
    with open(abspath, mode=mode) as fh:
        return fh.read()


class TokenHelper:

    def __init__(self):
        self.data = jwk_from_dict(json.loads(load_key_data('oct.json', 'r')))
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
        'data-toggle': 'table',
        'data-pagination': 'true',
        'data-show-columns': 'true',
        'data-multiple-select-row': 'true',
        'data-click-to-select': 'true',
        'overflow-y': 'scroll'} # html_attrs probably don't do anything


class Student(object):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email


class GroupTable(Table):
    classes = ['table']
    thead_classes = ['thead-dark']
    id = Col('id')
    name = Col('name')
    html_attrs = {
        'data-toggle': 'table',
        'data-search': 'true',
        'data-search-on-enter-key': 'true',
        'data-show-columns': 'true',
        'data-multiple-select-row': 'true',
        'data-click-to-select': 'true',
        'data-pagination': 'true'}


class Group(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class GroupUserTable(Table):
    classes = ['table']
    thead_classes = ['thead-dark']
    id = Col('id')
    username = Col('username')
    email = Col('email')
    html_attrs = {
        'data-toggle': 'table',
        'data-search': 'true',
        'data-search-on-enter-key': 'true',
        'data-show-columns': 'true',
        'data-multiple-select-row': 'true',
        'data-click-to-select': 'true',
        'data-pagination': 'true'}


class GroupUser(object):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email


class UserInfoTable(Table):
    classes = ['table']
    thead_classes = ['thead-dark']
    id = Col('id')
    username = Col('username')
    email = Col('email')


class UserInfo(object):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email


class ScenarioTable(Table):
    classes = ['table']
    thead_classes = ['thead_dark']
    id = Col('id')
    name = Col('name')
    created_at = Col('created_at')
    status = Col('status')


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

def check_role_view(mode): # check if view mode compatible with role (admin/inst/student)
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if not user.is_admin and not user.is_instructor:
        abort(403) # student's don't need their role checked
        return None # a student has no applicable role. does abort stop the calling/parent function?
    else:
        mode = request.args['mode']
        if mode not in ['studentView', 'instructorView', 'adminView']:
            abort(400) # only supported views
        elif user.is_instructor and not user.is_admin: # instructor only
            if mode == 'studentView':
                return True # return true since viewMode should be set
            elif mode == 'adminView':
                abort(403) # instructors can't choose adminView
            else:
                return False # return false since viewMode should be dropped
        elif user.is_admin:
            if mode in ['studentView', 'instructorView']:
                return True
            else:
                return False
        else:
            abort(403) # who are you?!
            return None

# --------

def generateNavElements(role, view): # generate all navigational elements
    """Makes decisions and calls correct generators for navigational links based on role."""
    views = None
    links = None
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
    views = [create_view('?mode=adminView', 'Admin View'),
             create_view('?mode=instructorView', 'Instructor View'),
             create_view('?mode=studentView', 'Student View')]

    return views


def genInstructorViews():
    """Generate 'select view' elements for instructors."""
    views = [create_view('?mode=instructorView', 'Instructor View'),
             create_view('?mode=studentView', 'Student View')]

    return views


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
    else:
        return None


def genInstructorLinks(view):
    """Generate links for instructors based on selected view."""
    if view == 'studentView':
        return genStudentLinks()
    elif not view:
        dashboard = create_link('dashboard.instructor', 'fa-desktop', 'Instructor Dashboard')
        scenarios = create_link('dashboard.scenarios', 'fa-align-justify', 'Scenarios')
        return [dashboard, scenarios]
    else:
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
    enr = db_ses.query(GroupUsers.group_id).filter(ScenarioGroups.scenario_id == d)\
        .filter(GroupUsers.group_id == ScenarioGroups.group_id).filter(GroupUsers.user_id == n).first()
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
        5: "ERROR"
    }
    return statSwitch[s]


def descGetter(t):
    t = t.lower().replace(" ", "_")
    with open('./scenarios/prod/' + t + '/' + t + '.yml', 'r') as yml:  # edurange_refactored/scenarios/prod
        document = yaml.full_load(yml)
        for item, doc in document.items():
            if item == 'Description':
                d = doc
    return d


def tempMaker(d, i):
    db_ses = db.session
    # status
    stat = db_ses.query(Scenarios.status).filter(Scenarios.id == d).first()
    stat = statReader(stat[0])
    # owner name
    oName = db_ses.query(User.username).filter(Scenarios.id == d).filter(Scenarios.owner_id == User.id).first()
    oName = oName[0]
    # description
    t = db_ses.query(Scenarios.description).filter(Scenarios.id == d).first()
    t = t[0]
    desc = descGetter(t)
    # name
    nom = db_ses.query(Scenarios.name).filter(Scenarios.id == d).first()
    nom = nom[0]
    if i == "i":
        # creation time
        bTime = db_ses.query(Scenarios.created_at).filter(Scenarios.id == d).first()
        bTime = bTime[0]
        return stat, oName, bTime, desc, t, nom
    else:
        return stat, oName, desc, t, nom

#
