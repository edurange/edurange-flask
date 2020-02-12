# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, redirect, session
from flask_login import login_required
from .models import User


blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")

@blueprint.route("/admin")
def adminPanel():
    number = session.get('_user_id')
    user = User.query.filter_by(id=number).first()
    if user.is_admin:
        return render_template('users/admin.html')
    return redirect('/')

