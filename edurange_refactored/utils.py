"""Helper utilities and decorators."""
from flask import flash
from flask_table import Table, Col


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)

class StudentTable(Table):
    classes = ['table']
    thead_classes = ['thead-dark']
    id = Col('id')
    username = Col('username')
    email = Col('email')
    html_attrs={
        'data-toggle': 'table',
        'data-pagination': 'true',
        'data-show-columns': 'true',
        'overflow-y': 'scroll'}

    def get_tr_attrs(self, item):
        return {'class': 'clickable-row'}

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
    html_attrs={
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
    html_attrs={
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
