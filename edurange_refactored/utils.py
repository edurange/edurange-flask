"""Helper utilities and decorators."""
from flask import flash
from flask_table import Table, Col, BoolCol
from wtforms.fields import BooleanField
from jwt.jwa import HS256
from jwt.jwk import jwk_from_dict, OctetJWK

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

class CheckCol(Col):
    def td_format(self, content):
        return '<div class="form-check">\n\t<input type="checkbox" class="form-check-input" value="">\n</div>'


class StudentTable(Table):
    classes = ['table']
    thead_classes = ['thead-dark']
    state = CheckCol('')
    id = Col('id')
    username = Col('username')
    email = Col('email')
    html_attrs = {
        'data-toggle': 'table',
        'data-pagination': 'true',
        'data-show-columns': 'true',
        'data-multiple-select-row': 'true',
        'data-click-to-select': 'true',
        'overflow-y': 'scroll'}


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
