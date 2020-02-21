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
    u_id = Col('id')
    u_name = Col('username')
    email = Col('email')

class Student(object):
    def __init__(self, u_id, u_name, email):
        #will have to change parameters
        self.u_id = u_id
        self.u_name = u_name
        self.email = email

