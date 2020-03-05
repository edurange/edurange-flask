# -*- coding: utf-8 -*-
"""User views."""
from flask import abort, Blueprint, flash, redirect, render_template, request, url_for, session
from flask_login import login_required
from edurange_refactored.user.forms import EmailForm, GroupForm, GroupFinderForm
from .models import User, StudentGroups, GroupUsers
from .models import generate_registration_code as grc
from ..utils import StudentTable, GroupTable, GroupUserTable, flash_errors
from edurange_refactored.tasks import send_async_email
from edurange_refactored.extensions import db

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

@blueprint.route("/admin", methods=['GET', 'POST'])
@login_required
def adminPanel():
    check_admin()
    students = User.query.all()
    stuTable = StudentTable(students)
    groups = StudentGroups.query.all()
    groTable = GroupTable(groups)
    if request.method == 'GET':
        form = EmailForm()
        form1 = GroupForm()
        form2 = GroupFinderForm()
        return render_template('users/admin.html', stuTable=stuTable, groTable=groTable, form=form, form1=form1, form2=form2)
    elif request.form.get('to') is not None:
        form = EmailForm(request.form)
        if form.validate_on_submit():
            email_data = {
                'subject' : form.subject.data,
                'to': form.to.data,
                'body': form.body.data
            }
            email = form.email.data
            if request.form['submit'] == 'Send':
                send_async_email.delay(email_data)
                flash('Sending email to {0}'.format(email))
            else:
                send_async_email.apply_async(args=[email_data], countdown=60)
                flash('An email will be sent to {0} in one minute.'.format(email))
            return redirect(url_for('user.adminPanel'))

    elif request.form.get('name') is not None:
        form = GroupForm(request.form)
        if form.validate_on_submit():
            code = grc()
            name = form.name.data
            StudentGroups.create(name=name, owner_id = session.get('_user_id'), code=code)
            flash('Created group {0}'.format(name))

            return redirect(url_for('user.adminPanel'))

    elif request.form.get('group') is not None:
        form = GroupFinderForm(request.form)
        if form.validate_on_submit():
            db_ses = db.session
            name = form.group.data
            groupUsers = db_ses.query(User.id, User.username, User.email, StudentGroups, GroupUsers).filter(StudentGroups.name == name).filter(StudentGroups.id == GroupUsers.group_id).filter(GroupUsers.user_id == User.id)
            groUTable = GroupUserTable(groupUsers)
            return render_template('users/admin.html', stuTable=stuTable, groTable=groTable, groUTable=groUTable, form=form)
        else:
            flash_errors(form)
        return redirect(url_for('user.adminPanel'))
#TODO: add function for adding users to groups
