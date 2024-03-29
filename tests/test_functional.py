# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from flask import url_for

from edurange_refactored.user.models import StudentGroups, User, GroupUsers

from .factories import GroupFactory, UserFactory


class TestLoggingIn:
    """Login."""

    def test_can_log_in_returns_200(self, user, testapp):
        """Login successful."""
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms["loginForm"]
        form["username"] = user.username
        form["password"] = "myprecious"
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        """Show alert on logout."""
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms["loginForm"]
        form["username"] = user.username
        form["password"] = "myprecious"
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for("public.logout")).follow()
        # sees alert
        assert "You are logged out." in res

    def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
        """Show error if password is incorrect."""
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form, password incorrect
        form = res.forms["loginForm"]
        form["username"] = user.username
        form["password"] = "wrong"
        # Submits
        res = form.submit()
        # sees error
        assert "Invalid password" in res

    def test_sees_error_message_if_username_doesnt_exist(self, user, testapp):
        """Show error if username doesn't exist."""
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form, password incorrect
        form = res.forms["loginForm"]
        form["username"] = "unknown"
        form["password"] = "myprecious"
        # Submits
        res = form.submit()
        # sees error
        assert "Unknown user" in res


class TestRegistering:
    """Register a user."""

    def test_can_register(self, user, testapp):
        """Register a new user."""
        # Goes to homepage
        res = testapp.get("/")
        # Check Number of Users
        old_count = len(User.query.all())
        # Clicks Create Account button
        res = res.click("Register")
        # Fills out the form
        form = res.forms["registerForm"]
        form["username"] = "foobar"
        form["email"] = "foo@bar.com"
        form["password"] = "secret"
        form["confirm"] = "secret"
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200
        # A new user was created
        assert len(User.query.all()) == old_count + 1

    def test_sees_error_message_if_passwords_dont_match(self, user, testapp):
        """Show error if passwords don't match."""
        # Goes to registration page
        res = testapp.get(url_for("public.register"))
        # Fills out form, but passwords don't match
        form = res.forms["registerForm"]
        form["username"] = "foobar"
        form["email"] = "foo@bar.com"
        form["password"] = "secret"
        form["confirm"] = "secrets"

        # Submits
        res = form.submit()
        # sees error message
        assert "Passwords must match" in res

    def test_sees_error_message_if_user_already_registered(self, user, testapp):
        """Show error if user already registered."""
        user = UserFactory(active=True)  # A registered user
        user.save()
        # Goes to registration page
        res = testapp.get(url_for("public.register"))
        # Fills out form, but username is already registered
        form = res.forms["registerForm"]
        form["username"] = user.username
        form["email"] = "foo@bar.com"
        form["password"] = "secret"
        form["confirm"] = "secret"

        # Submits
        res = form.submit()
        # sees error
        assert "Username already registered" in res


class TestGroupManagement:
    def test_can_create_group(self, admin, testapp):
        """Can create a group"""
        # Test group creation without ajax
        res = testapp.get(url_for("dashboard.admin"))
        old_count = len(StudentGroups.query.all())
        form = res.forms["createGroup"]
        form["name"] = "Test Group 1"
        form["size"] = 0
        res = form.submit(name="create")
        assert res.status_code == 200
        assert len(StudentGroups.query.all()) == old_count + 1
        assert "*Save these pairs" not in res

        # Test group creation with ajax
        old_count = len(StudentGroups.query.all())
        data = {"name": "Test Group 2", "create": "Create", "size": 0} # data packaged as it is in javascript on admin page
        headers = [('X-Requested-With', 'XMLHttpRequest')] # headers for ajax request
        res = testapp.post(url_for("dashboard.admin"), data, headers)
        assert res.status_code == 200
        assert len(StudentGroups.query.all()) == old_count + 1
        assert "*Save these pairs" not in res

    def test_can_generate_group(self, admin, testapp):
        """Can generate group of x temporary accounts"""
        # Test group generation without ajax
        res = testapp.get(url_for("dashboard.admin"))
        old_count = len(StudentGroups.query.all())
        form = res.forms["createGroup"]
        form["name"] = "Test Group 1"
        form[None] = True # check box for group generation
        form["size"] = 5  # generate group of size 5
        res = form.submit(name="create")
        assert res.status_code == 200
        assert len(StudentGroups.query.all()) == old_count + 1
        gid = StudentGroups.query.filter_by(name='Test Group 1').first()
        gid = gid.id
        assert len(GroupUsers.query.filter_by(group_id=gid).all()) == 5
        assert "*Save these pairs" in res

        # Test group generation with ajax
        old_count = len(StudentGroups.query.all())
        data = {"name": "Test Group 2", "create": "Create", "size": 10}
        headers = [('X-Requested-With', 'XMLHttpRequest')]
        res = testapp.post(url_for("dashboard.admin"), data, headers)
        assert res.status_code == 200
        assert len(StudentGroups.query.all()) == old_count + 1
        gid = StudentGroups.query.filter_by(name='Test Group 2').first()
        gid = gid.id
        assert len(GroupUsers.query.filter_by(group_id=gid).all()) == 10
        assert "*Save these pairs" in res

