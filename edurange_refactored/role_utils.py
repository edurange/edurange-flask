from flask_login import current_user
from werkzeug.exceptions import abort

from edurange_refactored.extensions import db
from edurange_refactored.user.models import User, Scenarios, GroupUsers, ScenarioGroups


def check_admin():
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if not user.is_admin:
        abort(403)


def check_instructor():
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if not user.is_instructor:
        abort(403)


def check_privs():
    number = current_user.id
    user = User.query.filter_by(id=number).first()
    if not user.is_instructor and not user.is_admin:
        abort(403)


def checkEx(d):
    db_ses = db.session
    scenId = db_ses.query(Scenarios).get(d)
    if scenId is not None:
        return True
    else:
        return False


def return_roles():
    number = current_user.id
    user = User.query.filter_by(id=number).first()

    admin, instructor = user.is_admin, user.is_instructor

    return admin, instructor


def checkEnr(d):
    db_ses = db.session
    n = current_user.id
    enr = (
        db_ses.query(GroupUsers.group_id)
            .filter(ScenarioGroups.scenario_id == d)
            .filter(GroupUsers.group_id == ScenarioGroups.group_id)
            .filter(GroupUsers.user_id == n)
            .first()
    )
    if enr is not None:
        return True
    else:
        return False
