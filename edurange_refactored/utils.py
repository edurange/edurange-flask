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
        'data-multiple-select-row': 'true',
        'data-click-to-select': 'true',
        'overflow-y': 'scroll'}
    def addCheck(self):
        self.add_column('State',
            Col(
                'state',
                column_html_attrs={'data-checkbox': 'true'}
            )
        )


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

#TODO: fix html_attrs, make row selection work at least

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

