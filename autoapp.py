# -*- coding: utf-8 -*-
"""Create an application instance."""
from edurange_refactored.app import create_app
from edurange_refactored.user.models import User, StudentGroups
from edurange_refactored.extensions import db
import os
from flask import session
from flask_login import current_user
app = create_app()
app.app_context().push()
db.create_all()

@app.context_processor
def utility_processor():
    def navigation(role, view=None):
        if role in ['a', 'a/i'] and not view:
            return (('public.home', 'Home'), ('dashboard.admin', 'Admin Dashboard'), ('dashboard.scenarios', 'Scenarios'), ('public.about', 'About'))
        elif (role == 'i' and not view) or (role in ['a', 'a/i'] and view == 'instructorView'):
            return (('public.home', 'Home'), ('dashboard.instructor', 'Instructor Dashboard'), ('dashboard.scenarios', 'Scenarios'), ('public.about', 'About'))
        elif (role is not None) or (role in ['a', 'a/i', 'i'] and view == 'studentView'):
            return (('public.home', 'Home'), ('dashboard.student', 'Dashboard'), ('public.about', 'About'))
        else:
            return (('public.home', 'Home'), ('public.about', 'About'))
    return dict(navigation=navigation)


def create_admin():
    username=os.environ['USERNAME']
    email=os.environ['EMAIL']
    password=os.environ['PASSWORD']
    User.create(username=username,
                email=email,
                password=password,
                active=True,
                is_admin=True,
                is_instructor=True)

def create_all_group():
    StudentGroups.create(name="ALL",
                         owner_id=a_id,
                         code="",
                         hidden=True)

def Aid():
    #number = session.get('_user_id')
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
            return 'a/i' # this option may not be needed
        elif user.is_admin:
            return 'a'
        elif user.is_instructor:
            return 'i'
        else:
            return False # false role --> student
    else:
        return None # no role --> not logged in


admin = User.query.limit(1).all()
print(admin)
print(admin)
print(admin)
if not admin:
    create_admin()

group = StudentGroups.query.limit(1).all()
admin = User.query.filter_by(username=os.environ['USERNAME']).first()
a_id = admin.get_id()
if not group:
    create_all_group()
app.jinja_env.globals.update(Aid=Aid)
app.jinja_env.globals.update(Iid=Iid)
app.jinja_env.globals.update(get_role=get_role)

