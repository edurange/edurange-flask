from flask_login import current_user
from werkzeug.exceptions import abort

from edurange_refactored.extensions import db
from edurange_refactored.user.models import GroupUsers, ScenarioGroups, Scenarios, User


def check_admin():
    user = User.query.filter_by(id=current_user.id).first()

    if not user.is_admin:
        abort(403)


def check_instructor():
    user = User.query.filter_by(id=current_user.id).first()

    if not user.is_instructor:
        abort(403)


def check_privs():
    user = User.query.filter_by(id=current_user.id).first()

    if not user.is_instructor and not user.is_admin:
        abort(403)


def scenario_exists(scenarioId):
    scenario = db.session.query(Scenarios).get(scenarioId)

    return bool(scenario)


def student_has_access(scenarioId):
    access = db.session.query(GroupUsers.group_id) \
                .filter(ScenarioGroups.scenario_id == scenarioId) \
                .filter(GroupUsers.group_id == ScenarioGroups.group_id) \
                .filter(GroupUsers.user_id == current_user.id) \
                .first()

    return bool(access)


def return_roles():
    user = User.query.filter_by(id=current_user.id).first()

    return user.is_admin, user.is_instructor
