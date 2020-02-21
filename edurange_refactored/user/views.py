# -*- coding: utf-8 -*-
"""User views."""
from flask import abort, Blueprint, render_template, session
from flask_login import login_required
from .models import User
from ..utils import StudentTable, Student

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")

# WARNING:
# This check is actually vulnerable to attacks.
# Since we're retrieving user id from the session request variables, it can be spoofed
# Although it requires knowledge of the admin user_id #, it will often just be '1'
# TODO: Harden check_admin()

def check_admin():
    number = session.get('_user_id')
    user = User.query.filter_by(id=number).first()
    if not user.is_admin:
        abort(403)

@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")

@blueprint.route("/admin")
@login_required
def adminPanel():
    check_admin()
    students = User.query.all()
    table = StudentTable(students)
    return render_template('users/admin.html')

