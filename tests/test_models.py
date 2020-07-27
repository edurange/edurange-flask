# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest
from sqlalchemy import exc

from edurange_refactored.user.models import StudentGroups, User
from edurange_refactored.user.models import generate_registration_code as grc

from .factories import GroupFactory, UserFactory


@pytest.mark.usefixtures("db")
class TestUser:
    """User tests."""

    def test_get_by_id(self):
        """Get user by ID."""
        user = User("foo", "foo@bar.com")
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        """Test creation date."""
        user = User(username="foo", email="foo@bar.com")
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self):
        """Test null password."""
        user = User(username="foo", email="foo@bar.com")
        user.save()
        assert user.password is None

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password="myprecious")
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password("myprecious")

    def test_check_password(self):
        """Check password."""
        user = User.create(username="foo", email="foo@bar.com", password="foobarbaz123")
        assert user.check_password("foobarbaz123") is True
        assert user.check_password("barfoobaz") is False


@pytest.mark.usefixtures("db")
class TestGroup:
    """Group tests."""

    def test_get_by_id(self):
        """Get group by ID."""
        group = StudentGroups.create(name="testgroup", owner_id=1)
        group.save()

        retrieved = StudentGroups.get_by_id(group.id)
        assert retrieved == group

    def test_groupname_is_unique(self, db):
        """Test unique group names only"""
        group = StudentGroups.create(name="testgroup", owner_id=1, code=grc())
        group.save()
        group2 = None
        with pytest.raises(exc.IntegrityError):
            group2 = StudentGroups.create(name="testgroup", owner_id=2, code=grc())
            group2.save()

        assert group is not None
        assert group2 is None

    def test_hidden_defaults_to_false(self):
        """Test that hidden attribute defaults to false"""
        group = StudentGroups.create(name="testgroup", owner_id=1, code=grc())
        group.save()

        assert group.hidden is False

    def test_factory(self, db):
        """Test group factory"""
        group = GroupFactory()
        db.session.commit()
        assert bool(group.name)
        assert bool(group.owner_id)
        assert bool(group.owner)
        assert bool(group.hidden) is False
