# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from factory import PostGenerationMethodCall, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from edurange_refactored.database import db
from edurange_refactored.user.models import User, StudentGroups


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: f"user{n}")
    email = Sequence(lambda n: f"user{n}@example.com")
    password = PostGenerationMethodCall("set_password", "example")
    active = True
    is_admin = False

    class Meta:
        """Factory configuration."""

        model = User

class GroupFactory(BaseFactory):
    """Group factory."""


    name = Sequence(lambda n: f"group{n}")
    owner_id = Sequence(lambda n: f"{n}")
    owner = SubFactory(UserFactory, username="ownerName")
    hidden = False

    class Meta:
        """Factory configuration."""

        model = StudentGroups
