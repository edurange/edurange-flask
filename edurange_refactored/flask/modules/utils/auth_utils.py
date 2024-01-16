from flask import (
    request,
    session,
    jsonify,
    g
)
from edurange_refactored.user.models import User
from functools import wraps
from flask_jwt_simple import decode_jwt
from edurange_refactored.user.models import GroupUsers, StudentGroups, User


###########
#  This `@jwt_and_csrf_required()` decorator function should be used on ALL 
#  non-legacy routes except those not requiring login.
###########
def jwt_and_csrf_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        
        # CSRF check (dev)
        client_CSRF = request.headers.get('X-XSRF-TOKEN')
        if not client_CSRF: return jsonify({"error": "no client csrf request denied"}), 418
        server_CSRF = session.get('X-XSRF-TOKEN')
        if not server_CSRF: return jsonify({"error": "no server csrf request denied"}), 418
        if client_CSRF != server_CSRF:  return jsonify({"error": "csrf bad match"}), 418
        
        
        # CSRF check (prod)
        # client_CSRF = request.headers.get('X-CSRFToken')
        # edurange3_csrf = session.get('X-XSRF-TOKEN')
        # if (
        #     not edurange3_csrf
        #     or not client_CSRF
        #     or client_CSRF != edurange3_csrf):
        #         return jsonify({"error": "csrf request denied"}), 418
        
        # JWT check
        token = request.cookies.get('edurange3_jwt')
        if not token: return jsonify({"error": "jwt request denied"}), 418
        try:

            validated_jwt_token = decode_jwt(token)  # check if signature still valid
            decoded_payload = validated_jwt_token["sub"]

            g.current_username = decoded_payload["username"]  
            g.current_user_id = decoded_payload["user_id"] 
            g.current_user_role = decoded_payload["user_role"] 
            # Places values in special Flask `g` object which ONLY lasts for life of request
            # The `g` object can be accessed by any routes decorated with jwt_and_csrf_required()
            # To avoid auth 'misses', use the `g` object any time the values are needed

        except Exception as err:
            return jsonify({"error": "some request denied"}), 418

        return fn(*args, **kwargs)
    
    return wrapper

def register_user(validated_registration_data):
    data = validated_registration_data
    User.create(
            username=data.username,
            email=data.email,
            password=data.password,
            active=True,
    )
       
    group = StudentGroups.query.filter_by(code=data.code).first()
    user = User.query.filter_by(username=data.username).first()
    group_id = group.get_id()
    user_id = user.get_id()
    GroupUsers.create(user_id=user_id, group_id=group_id)
