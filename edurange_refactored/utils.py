# -*- coding: utf-8 -*-
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

class Group(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

