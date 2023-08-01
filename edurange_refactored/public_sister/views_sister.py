
from flask import Blueprint

from flask_login import current_user, login_required, login_user, logout_user
from jwt import JWT
from jwt.exceptions import JWTDecodeError
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    url_for,
    jsonify

)

from edurange_refactored.extensions import bcrypt, login_manager
from edurange_refactored.public.forms import (
    LoginForm,LoginFormSister,
    RequestResetPasswordForm,
    RestorePasswordForm,
)
from edurange_refactored.tasks import test_send_async_email
from edurange_refactored.user.forms import RegisterForm
from edurange_refactored.user.models import GroupUsers, StudentGroups, User
from edurange_refactored.utils import TokenHelper, flash_errors

# blueprint = Blueprint("public", __name__, static_folder="../static")
jwtToken = JWT()
helper = TokenHelper()
oct_data = helper.get_data()

blueprint_routing_sister = Blueprint('public_sister', __name__)


@blueprint_routing_sister.route("/home_sister/", defaults={'path': ''}, methods=["GET"])
@blueprint_routing_sister.route("/home_sister/<path:path>")
def catch_all(path):
    form = LoginForm(request.form)
    return render_template("public/home_sister.html", form=form)

@blueprint_routing_sister.route("/home_sister/login", methods=["POST"])
def login_sister():
    form = LoginFormSister()
    if form.validate_on_submit():
        login_user(form.user)
        return jsonify({
            "login_success": "true",
        })
    else:
        return jsonify({"login_success": "false"})
  