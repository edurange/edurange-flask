


from flask import Blueprint

import secrets

from flask_login import current_user, login_required, login_user, logout_user
from jwt import JWT
from jwt.exceptions import JWTDecodeError
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    jsonify
)

from edurange_refactored.user.models import User
from edurange_refactored.api.schemas.ma_user import LoginSchema
from edurange_refactored.public.forms import LoginForm
# from edurange_refactored.tasks import test_send_async_email
from edurange_refactored.utils import TokenHelper
from edurange_refactored.extensions import db
from marshmallow import ValidationError

from edurange_refactored.public_sister import views_sister_dbTester

jwtToken = JWT()
helper = TokenHelper()
oct_data = helper.get_data()
db_ses = db.session
csrf_token_sister = secrets.token_hex(32)

blueprint_routing_sister = Blueprint('public_sister', __name__)

@blueprint_routing_sister.before_request
def ensure_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)

@blueprint_routing_sister.errorhandler(ValidationError)
def handle_marshmallow_error(err):
    return jsonify(err.messages), 400

@blueprint_routing_sister.route("/home_sister/login", methods=["POST"])
def login_sister():

    data = request.json
    csrf_token_client = request.headers.get('csrf_token_sister')
    csrf_token_server = session['csrf_token']

    if csrf_token_client != csrf_token_server:
        return jsonify({"error": f"invalid request"}), 400

    validation_schema = LoginSchema()  # instantiate validation schema
    validated_data = validation_schema.load(data) # runs data through validator, returns error if bad
    validated_user = validation_schema.dump(vars(User.query.filter_by(username=validated_data["username"]).first()) ) # retrieve schema-designated data and format it
    return jsonify(validated_user)


@blueprint_routing_sister.route("/home_sister/", defaults={'path': ''}, methods=["GET"])
@blueprint_routing_sister.route("/home_sister/<path:path>")
def catch_all(path):
    form = LoginForm(request.form)
    return render_template("public/home_sister.html",csrf_token_sister=session['csrf_token'])

@blueprint_routing_sister.route("/home_sister/skeletonkey", methods=['GET', 'POST'])
def skeletonkey():
    return jsonify( views_sister_dbTester.get_instructor_data() )
