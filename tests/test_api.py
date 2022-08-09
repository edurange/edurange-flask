# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt
import os
import sys

import pytest
from sqlalchemy import exc

from edurange_refactored.user.models import Responses, StudentGroups, User
from edurange_refactored.user.models import generate_registration_code as grc

from .factories import GroupFactory, UserFactory

class TestValidateUsage:
    def test_parsable_url(self, admin, testapp):
        res = testapp.get("/api/get_content/hello", expect_errors=True)
        assert res.status_code == 400
        assert "Bad Request" in res

        res = testapp.get("/api/get_state/hello", expect_errors=True)
        assert res.status_code == 400
        assert "Bad Request" in res

        res = testapp.post("/api/post_ans/hello", {}, expect_errors=True)
        assert res.status_code == 400
        assert "Bad Request" in res

    def test_scenario_does_not_exist(self, admin, testapp):
        res = testapp.get("/api/get_content/1", expect_errors=True)
        assert res.status_code == 404
        assert "Scenario does not exist" in res

        res = testapp.get("/api/get_state/1", expect_errors=True)
        assert res.status_code == 404
        assert "Scenario does not exist" in res

        form = {
            "question":"",
            "response":"",
            "scenario":""
        }
        res = testapp.post("/api/post_ans/1", form, expect_errors=True)
        assert res.status_code == 404
        assert "Scenario does not exist" in res

    def test_need_login(self, testapp):
        res = testapp.get("/api/get_content/1", expect_errors=True)
        assert res.status_code == 401
        assert "not authorized" in res

        res = testapp.get("/api/get_state/1", expect_errors=True)
        assert res.status_code == 401
        assert "not authorized" in res

        res = testapp.post("/api/post_ans/1", {}, expect_errors=True)
        assert res.status_code == 401
        assert "not authorized" in res

class TestGetContent:
    def test_user_can_get_content(self, user, testapp, scenario):
        res = testapp.get("/api/get_content/1")
        assert res.status_code == 200
        assert "Question1" in res

    def test_admin_can_get_content(self, admin, testapp, scenario):
        res = testapp.get("/api/get_content/1")
        assert res.status_code == 200
        assert "Question1" in res
    
class TestGetState:
    def test_admin_can_get_state(self, admin, testapp, scenario):
        res = testapp.get("/api/get_state/1")
        assert res.status_code == 200
        assert "CurrentScore" in res
    
    def test_user_can_get_state(self, user, testapp, scenario):
        res = testapp.get("/api/get_state/1")
        assert res.status_code == 200
        assert "CurrentScore" in res
    
class TestPostAns:
    def test_post_ans(self, admin, testapp, scenario, db):
        form = {
            "question":"",
            "response":"",
            "scenario":""
        }
        res = testapp.post("/api/post_ans/1", form, expect_errors=True)
        assert res.status_code == 200
        resp = Responses.query.limit(1).all()
        pytest.fail(str(resp))
