
from flask import abort
from edurange_refactored.extensions import db, bcrypt
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError, validate, validates_schema
from marshmallow.fields import String
from edurange_refactored.user.models import GroupUsers, ScenarioGroups, Scenarios, StudentGroups, User, Notification
ma = Marshmallow()
db_ses = db.session

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

        if (
            not user 
            or not bcrypt.check_password_hash(user.password, password_plain_input)
            ):
                abort(418)  

    class Meta:
        model = User
        # exclude = ["id"]

class RegistrationSchema(ma.SQLAlchemyAutoSchema):
    banned_names = ["root", "ubuntu", "nobody", "ec2user", "user", "student", "guest", '' ]
    
    email = String(required=True, validate=[validate.Email(error="Please use a valid email address")])
    
    username = String(required=True, validate=[
        validate.Length(min=3, max=25, error="Username must be between 3 and 25 characters"),
        validate.ContainsNoneOf(banned_names, error="Nice try bucko, use a different name"),
        validate.Regexp('^\w+-?\w+-?\w+$', error="Username must be alphanumeric")
        ])
    
    code = String(required=True, validate=[validate.Length(min=0, max=8)])
    password = String(required=True, validate=[validate.Length(min=6, max=40)])
    # confirm_password = String(required=True, validate=[validate.Equal(password, error="Passwords do not match")])
    confirm_password = String(required=True)
    
    @validates_schema
    def validate_registration(self, data, **kwargs):
        username_input = data.get("username")
        password_input = data.get("password")
        confirm_password_input = data.get("confirm_password")
        email_input = data.get("email")
        code_input = data.get("code")

        if password_input != confirm_password_input:
            raise ValidationError("Passwords do not match")
        
        if password_input == confirm_password_input:
            print('pws match')

        user = db_ses.query(User).filter_by(username=username_input).first()
        print(user)
        if user != None:
            print("user already exists! aborting...")
            abort(418)

    class Meta:
        model = User






