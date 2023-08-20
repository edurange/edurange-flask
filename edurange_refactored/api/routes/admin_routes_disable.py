
from flask import (
    Blueprint,
    request,
    session,
    jsonify,
    make_response,
)
from edurange_refactored.user.models import User
from edurange_refactored.extensions import db, csrf_protect
from edurange_refactored.api.utils.db_devHelper import (
    get_user,
    get_users,
    get_groups,
    get_group_users,
    get_scenarios,
    get_scenario_groups,
    get_student_responses,
    get_instructor_data,  # gets all the previous
)

db_ses = db.session
blueprint_edurange3_admin = Blueprint('edurange3_admin', __name__)
csrf_protect.exempt(blueprint_edurange3_admin)

@blueprint_edurange3_admin.route("/edurange3/api/admin_test")
def admin_test():
    return jsonify ({"message":"this is /edurange3/api/admin_test"})