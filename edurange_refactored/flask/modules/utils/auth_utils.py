from flask import (
    request,
    session,
    jsonify,
    g
)
from edurange_refactored.user.models import User
from functools import wraps
from flask_jwt_simple import decode_jwt

###########
#  This `@jwt_and_csrf_required()` decorator function should be used on ALL non-legacy routes except those not requiring login.
###########
def jwt_and_csrf_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        
        # CSRF check (dev)
        csrf_token_client = request.headers.get('X-XSRF-TOKEN')
        if not csrf_token_client: return jsonify({"error": f"no client csrf request denied"}), 418
        edurange3_csrf = session.get('X-XSRF-TOKEN')
        if not edurange3_csrf: return jsonify({"error": "no server csrf request denied"}), 418
        if csrf_token_client != edurange3_csrf:  return jsonify({"error": "csrf bad match"}), 418
        
        
        # CSRF check (prod)
        # csrf_token_client = request.headers.get('X-CSRFToken')
        # edurange3_csrf = session.get('X-XSRF-TOKEN')
        # if (
        #     not edurange3_csrf
        #     or not csrf_token_client
        #     or csrf_token_client != edurange3_csrf):
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