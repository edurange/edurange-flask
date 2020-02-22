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
    id = Col('id')
    username = Col('username')
    email = Col('email')


class Student(object):
    def __init__(self):
        self.id = id
        self.username = username
        self.email = email
