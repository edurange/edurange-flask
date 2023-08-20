import secrets
from flask import (
    request,
    session,
    jsonify,
    g
)
from functools import wraps
from flask_jwt_simple import decode_jwt
# edurange3_csrf = secrets.token_hex(32)

###########
#  This `@jwt_and_csrf_required()` decorator function should be used on ALL non-legacy routes except those not requiring login.
###########
def jwt_and_csrf_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        
        # CSRF check
        csrf_token_client = request.headers.get('X-CSRFToken')
        edurange3_csrf = session.get('edurange3_csrf')
        
        if not csrf_token_client:
            return jsonify({"error": "Missing CSRF Token in header"}), 403
        if not edurange3_csrf or csrf_token_client != edurange3_csrf:
            return jsonify({"error": "Invalid CSRF Token"}), 403
        
        # JWT check
        token = request.cookies.get('edurange3-jwt')
        if not token:
            return jsonify({"error": "Missing Authorization Token"}), 401
        
        try:
            decoded_jwt_token = decode_jwt(token)
            g.decoded_jwt_token = decoded_jwt_token # places the token in this special Flask `g` object that only lasts for the life of the request
                                                    # but can be accessed by the routes with g.decoded_jwt_token.
                                                    # that variable should be used instead of decoding the cookie again, by convention.
                                                    # this ensures the value only will exist if it has been run through this process.
        except Exception as err:
            return jsonify({"error": str(err)}), 401

        return fn(*args, **kwargs)
    
    return wrapper