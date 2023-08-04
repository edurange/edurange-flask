# -*- coding: utf-8 -*-
"""Public forms."""
from datetime import datetime, timedelta, timezone

from flask_wtf import FlaskForm
from jwt import JWT
from jwt.exceptions import JWTDecodeError
from jwt.jwa import HS256
from jwt.utils import get_int_from_datetime
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from edurange_refactored.user.models import User
from edurange_refactored.utils import TokenHelper

jwtToken = JWT()
helper = TokenHelper()
oct_data = helper.get_data()


class LoginForm(FlaskForm):
    """Login form."""

    # username = ""
    # password = ""
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append("Unknown username")
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append("Invalid password")
            return False

        if not self.user.active:
            self.username.errors.append("User not activated")
            return False
        return True

class LoginFormSister(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(LoginFormSister, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginFormSister, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        
        if not self.user \
        or not self.user.check_password(self.password.data) \
        or not self.user.active:
            self.username.errors.append("Invalid Credentials")
            self.password.errors.append("Invalid Credentials")
            return False
        return True

class RequestResetPasswordForm(FlaskForm):
    """Request reset password form"""

    username = StringField(validators=None)
    password = PasswordField(validators=None)
    email = StringField(
        "Email Address", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RequestResetPasswordForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        self.user = User.query.filter_by(email=self.email.data).first()
        if not self.user:
            return False
        return True

    def get_email_data(self):
        token = jwtToken.encode(
            dict(
                iss="https://edurange.org/",
                email=self.user.email,
                iat=get_int_from_datetime(datetime.now(timezone.utc)),
                exp=get_int_from_datetime(
                    datetime.now(timezone.utc) + timedelta(hours=1)
                ),
            ),
            key=oct_data,
            alg="HS256",
        )
        email_data = {
            "subject": "Reset Password",
            "token": token,
            "email": self.user.email,
        }
        return email_data


class RestorePasswordForm(FlaskForm):
    """Restore password form"""

    user = None
    username = StringField(validators=None)
    email = StringField(validators=None)
    password = PasswordField("Password", validators=[DataRequired()])
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RestorePasswordForm, self).__init__(*args, **kwargs)
        # self.user = None
