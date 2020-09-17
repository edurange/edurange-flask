# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
import random
import string

from flask_login import UserMixin

from edurange_refactored.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)
from edurange_refactored.extensions import bcrypt

# import string
# import random


def generate_registration_code(size=8, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


class StudentGroups(UserMixin, SurrogatePK, Model):
    """"Groupts of Users"""

    __tablename__ = "groups"
    name = Column(db.String(40), unique=True, nullable=False)
    owner_id = reference_col("users", nullable=False)
    owner = relationship("User", backref="groups")
    code = Column(
        db.String(8), unique=True, nullable=True, default=generate_registration_code()
    )
    hidden = Column(db.Boolean(), nullable=False, default=False)


class GroupUsers(UserMixin, SurrogatePK, Model):
    """Users belong to groups"""

    ___tablename___ = "group_users"
    user_id = reference_col("users", nullable=False)
    user = relationship("User", backref="group_users")
    group_id = reference_col("groups", nullable=False)
    group = relationship("StudentGroups", backref="group_users")


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    is_instructor = Column(db.Boolean(), default=False)
    is_static = Column(db.Boolean(), default=False) # static: user belongs to one group only (for generated groups)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"


class Scenarios(UserMixin, SurrogatePK, Model):
    """An exercise  """

    __tablename__ = "scenarios"

    name = Column(db.String(40), unique=False, nullable=False)
    description = Column(db.String(80), unique=False, nullable=True)
    owner_id = reference_col("users", nullable=False)
    owner = relationship("User", backref="scenarios", lazy="subquery")
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    status = Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Scenario({self.name!r})>"


class ScenarioGroups(UserMixin, SurrogatePK, Model):
    """Groups associated with scenarios"""

    __tablename__ = "scenario_groups"
    group_id = reference_col("groups", nullable=False)
    group = relationship("StudentGroups", backref="scenario_groups")
    scenario_id = reference_col("scenarios", nullable=False)
    scenario = relationship("Scenarios", backref="scenario_groups")


class Responses(UserMixin, SurrogatePK, Model):
    """Student responses to scenario questions"""

    __tablename__ = "responses"
    user_id = reference_col("users", nullable=False)
    user = relationship("User", backref="responses")
    scenario_id = reference_col("scenarios", nullable=False)
    scenario = relationship("Scenarios", backref="responses")
    question = Column(db.Integer, default=0, nullable=False)
    student_response = Column(db.String(40), unique=False, nullable=True)
    correct = Column(db.Boolean(), default=False)
    response_time = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    attempt = Column(db.Integer, default=0, nullable=False)
    # learning objective field?

class BashHistory(UserMixin, SurrogatePK, Model):
    """Bash Histories, associated with users and scenarios"""

    __tablename__ = "bash_history"
    user_id = reference_col("users", nullable=False)
    user = relationship("User", backref="bash_history")
    scenario_id = reference_col("scenarios", nullable=False)
    scenario = relationship("Scenarios", backref="bash_history")
    response_time = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
