# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, AnyOf, Regexp, NoneOf
from .models import User, StudentGroups

from .models import StudentGroups, User


class RegisterForm(FlaskForm):
    """Register form."""

    banned_names = ["root", "ubuntu", "user", "student", "guest", "ec2-user", "nobody", '']
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25),
                                Regexp('^\w+-?\w+-?\w+$', message="must be alphanumeric"),
                                NoneOf(values=banned_names, message="not permitted, try a different one")]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    code = StringField(
        "Registration Code", validators=[DataRequired(), Length(min=0, max=8)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        if self.code.data:
            group = StudentGroups.query.filter_by(code=self.code.data).first()
            if not group:
                self.code.errors.append("Invalid registration code")
                return False
        return True


# ---------------------------------- (unused?)
class EmailForm(FlaskForm):
    """Email Form."""

    subject = StringField("Subject", validators=[DataRequired()])
    to = StringField("Recipient", validators=[DataRequired()])
    body = StringField("Body", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(EmailForm, self).validate()
        if not initial_validation:
            return False
        return True


# -----------------------------------------------------


class changeEmailForm(FlaskForm):
    """Change Email form."""
    address = StringField(
        "New Address", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )

    def __init__(self, *args, **kwargs):
        super(changeEmailForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(changeEmailForm, self).validate()
        if not initial_validation:
            return False
        email = User.query.filter_by(email=self.address.data).first()
        if email:
            self.address.errors.append("Email already registered")
            return False
        return True


class GroupForm(FlaskForm):
    """Create New Group Form"""
    name = StringField(
        "Group Name", validators=[DataRequired()]
    )
    size = IntegerField(
        "Group Size", validators=[
            NumberRange(min=0, max=60, message="Account generation may not surpass a count of 60 (and must be positive)")]
    )

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(GroupForm, self).validate()
        if not initial_validation:
            return False
        group = StudentGroups.query.filter_by(name=self.name.data).first()
        if group:
            self.name.errors.append("Group with this name already exists")
            return False
        return True


class addUsersForm(FlaskForm):
    """Adds selected users to a group"""

    add = StringField("Add", validators=[AnyOf(['true', 'false'], message="Do this by clicking the buttons")])
    uids = StringField("User IDs", validators=[DataRequired()])
    groups = StringField("Group Name", validators=[DataRequired()])

    # user id list

    def __init__(self, *args, **kwargs):
        super(addUsersForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(addUsersForm, self).validate()
        if not initial_validation:
            return False
        group = StudentGroups.query.filter_by(name=self.groups.data).first()
        if not group:
            self.groups.errors.append("Group with this name cannot be found")
        users = self.uids.data
        if self.uids.data[-1] == ",":
            self.uids.data = self.uids.data[:-1]  # slice last comma to avoid empty string after string split
            users = self.uids.data
        else:
            users = self.uids.data
        users = users.split(",")
        if '' in users or ' ' in users:
            self.uids.errors.append("User selection must be in comma-separated string. Ex: '1,2,15,30'")
            return False
        for id in users:
            if not isinstance(int(id), int):
                self.uids.errors.append("User selection must be in the form of integers (ID #'s) separated by commas. Ex: '1,2,15,30'")
                return False
        return True


class manageInstructorForm(FlaskForm):  # type1
    """Elevates user to an instructor"""

    uName = StringField("Username", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(manageInstructorForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(manageInstructorForm, self).validate()
        if not initial_validation:
            return False
        return True


class makeScenarioForm(FlaskForm):
    """Creates a Scenario"""

    scenario_name = StringField("Scenario", validators=[DataRequired()])

    scenario_group = StringField("Group", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(makeScenarioForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(makeScenarioForm, self).validate()
        if not initial_validation:
            return False
        return True


class modScenarioForm(FlaskForm):
    """Creates a Scenario"""

    sid = StringField("Scenario ID", validators=[DataRequired()])

    mod_scenario = StringField("Action", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(modScenarioForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(modScenarioForm, self).validate()
        if not initial_validation:
            return False
        return True


class scenarioResponseForm(FlaskForm):
    """records a students response to a scenario question"""

    scenario = StringField("Scenario", validators=[DataRequired()])

    question = StringField("Question", validators=[DataRequired()])

    response = StringField("Response", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(scenarioResponseForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(scenarioResponseForm, self).validate()
        if not initial_validation:
            return False
        return True


# -
class deleteGroupForm(FlaskForm):
    """designates a student group to be deleted"""

    group_name = StringField("Group Name", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(deleteGroupForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(deleteGroupForm, self).validate()
        if not initial_validation:
            return False
        return True


# -


class type1Form(FlaskForm):                 # GroupForm,    manageInstructorForm,   deleteStudentForm
    """Type 1 form, one string field"""
    string1 = StringField(
        "string1", validators=[DataRequired()]
    )                                       # name,         uName,                  stuName

    def __init__(self, *args, **kwargs):
        super(type1Form, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(type1Form, self).validate()
        if not initial_validation:
            return False
        return True


class type2Form(FlaskForm):                 # addUsersForm, makeScenarioForm,   modScenarioForm
    """Type 2 form, two string fields"""
    string1 = StringField(
        "string1", validators=[DataRequired()]
    )                                       # uids,         scenario_name,      sid

    string2 = StringField(
        "string2", validators=[DataRequired()]
    )                                       # groups,       scenario_group,     mod_scenario

    def __init__(self, *args, **kwargs):
        super(type2Form, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(type2Form, self).validate()
        if not initial_validation:
            return False
        return True


# -
