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


admin = User.query.limit(1).all()
if not admin:
    create_admin()

group = StudentGroups.query.limit(1).all()
admin = User.query.filter_by(username=os.environ["FLASK_USERNAME"]).first()
a_id = admin.get_id()
if not group:
    create_all_group(a_id)
