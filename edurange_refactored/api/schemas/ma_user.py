

from edurange_refactored.extensions import db, bcrypt
from flask_marshmallow import Marshmallow
from marshmallow import validate, ValidationError, validates_schema
from marshmallow.fields import String
from edurange_refactored.user.models import GroupUsers, ScenarioGroups, Scenarios, StudentGroups, User, Notification

ma = Marshmallow()
db_ses = db.session

class TestUser(db.Model):
    __tablename__ = 'users'

class LoginSchema(ma.SQLAlchemyAutoSchema):

    email = String(required=False)
    username = String(required=True, validate=[validate.Length(min=3, max=40) ])
    password = String(required=True, validate=[
        validate.Length(min=3, max=40),
        # validate.ContainsNoneOf[]
        ])
    
    @validates_schema
    def validate_login(self, data, **kwargs):

        username_input = data.get("username")
        password_plain_input = data.get("password")
        user = db_ses.query(User).filter_by(username=username_input).first()

        if not user or not bcrypt.check_password_hash(user.password, password_plain_input):
            raise ValidationError("invalid credentials")
    class Meta:
        model = User
        exclude = ["id"]