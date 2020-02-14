# -*- coding: utf-8 -*-
"""Create an application instance."""
from edurange_refactored.app import create_app
from edurange_refactored.user.models import User
import os

app = create_app()

admin = User.query.filter_by(username='admin').first()
if not admin:
    default_User()


def default_User():
    #
    username=os.environ['USERNAME']
    email=os.environ['EMAIL']
    password=os.environ['PASSWORD']
    #
    active=os.environ['ACTIVE']
    is_admin=os.environ['IS_ADMIN']
    is_instructor=os.environ['IS_INSTRUCTOR']

    default_user = User(unsername=username, email=email, password=password, active=active, is_admin=is_admin, is_instructor=is_instructor)
    db.session.add(default_user)
    db.session.commit()

