# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User


class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    code = StringField(
        "Registration Code", validators=[DataRequired(), Length(min=8, max=8)]
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
        return True


class EmailForm(FlaskForm):
    """Email Form."""
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    subject = StringField(
        "Subject", validators=[DataRequired()]
    )
    to = StringField(
        "Recipient", validators=[DataRequired()]
    )
    body = StringField(
        "Body", validators=[DataRequired()]
    )

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(EmailForm, self).validate()
        if not initial_validation:
            return False
        return True
