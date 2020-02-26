# -*- coding: utf-8 -*-
"""Create an application instance."""
from edurange_refactored.app import create_app
from edurange_refactored.user.models import User, StudentGroups
from edurange_refactored.extensions import db
import os
app = create_app()
app.app_context().push()
db.create_all()

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
                         code="")

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

