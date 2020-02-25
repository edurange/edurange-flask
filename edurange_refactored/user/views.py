# -*- coding: utf-8 -*-
"""User views."""
from flask import abort, Blueprint, redirect, render_template, request, url_for, session
from flask_login import login_required
from edurange_refactored.user.models import User
from edurange_refactored.user.forms import EmailForm
from edurange_refactored.utils import flash, StudentTable
from edurange_refactored.tasks import send_async_email

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
    table = StudentTable(students)
    if request.method == 'GET':
        form = EmailForm()
        return render_template('users/admin.html', table=table, form=form)
    else:
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

