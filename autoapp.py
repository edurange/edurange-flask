# -*- coding: utf-8 -*-
"""Create an application instance."""
from edurange_refactored.app import create_app
from edurange_refactored.user.models import User
import os

app = create_app()
app.app_context().push()

def create_admin():
    username=os.environ['FLASK_USERNAME']
    email=os.environ['EMAIL']
    password=os.environ['PASSWORD']
    
    User.create(username=username,
                email=email,
                password=password,
                active=True,
                is_admin=True,
                is_instructor=True)


admin = User.query.limit(1).all()
if not admin:
    create_admin()

