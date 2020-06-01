# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user

from edurange_refactored.extensions import login_manager
from edurange_refactored.public.forms import LoginForm
from edurange_refactored.user.forms import RegisterForm
from edurange_refactored.user.models import User, StudentGroups, GroupUsers
from edurange_refactored.utils import flash_errors

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = url_for("public.home")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        if form.code.data:
            group = StudentGroups.query.filter_by(code=form.code.data).first()
            user = User.query.filter_by(username=form.username.data).first()
            gid = group.get_id()
            uid = user.get_id()
            GroupUsers.create(user_id=uid, group_id=gid)
        else:
            group = StudentGroups.query.filter_by(name="ALL").first()
            gid = group.get_id()
            user = User.query.filter_by(username=form.username.data).first()
            uid = user.get_id()
            GroupUsers.create(user_id=uid, group_id=gid)
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)
