# -*- coding: utf-8 -*-
"""User views."""
from flask import abort, Blueprint, render_template, session
from flask_login import login_required
from .models import User


blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")

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
def adminPanel():
    check_admin()
    return render_template('users/admin.html')

