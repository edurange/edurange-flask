# -*- coding: utf-8 -*-
"""Create an application instance."""
from edurange_refactored.app import create_app
from edurange_refactored.user.models import User, StudentGroups
from edurange_refactored.extensions import db
from edurange_refactored.utils import generateNavElements
import os
from datetime import datetime

from flask import session
from flask_login import current_user

app = create_app()
app.app_context().push()
db.create_all()


@app.context_processor
def utility_processor():
    def navigation(role, view=session.get('viewMode')):
        return generateNavElements(role, view)
    return dict(navigation=navigation)


def create_admin():
    username = os.environ["FLASK_USERNAME"]
    email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]
    User.create(
        username=username,
        email=email,
        password=password,
        active=True,
        is_admin=True,
        is_instructor=True,
    )


def create_all_group(id):
    StudentGroups.create(name="ALL", owner_id=id, code="", hidden=True)


def Aid():
    # number = session.get('_user_id')
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if user.is_admin:
        return True
    return False


def Iid():
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if user.is_instructor:
        return True
    return False


def get_role():
    if current_user and current_user.is_authenticated:
        number = current_user.id
        user = User.query.filter_by(id=number).first()
        if user.is_admin and user.is_instructor:
            return "a/i"  # this option may not be needed
        elif user.is_admin:
            return "a"
        elif user.is_instructor:
            return "i"
        else:
            return 's'
    else:
        return None  # no role --> not logged in


admin = User.query.limit(1).all()
if not admin:
    create_admin()

group = StudentGroups.query.limit(1).all()
admin = User.query.filter_by(username=os.environ["FLASK_USERNAME"]).first()
a_id = admin.get_id()
if not group:
    create_all_group(a_id)
app.jinja_env.globals.update(Aid=Aid)
app.jinja_env.globals.update(Iid=Iid)
app.jinja_env.globals.update(get_role=get_role)


def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)

def timectime(s):
    return datetime.fromtimestamp(int(s))


app.jinja_env.filters["formatdatetime"] = format_datetime
app.jinja_env.filters["ctime"] = timectime
