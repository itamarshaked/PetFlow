from functools import wraps

from flask import g, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from services.user_service import get_or_create_auth0_user


def requires_any_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        # ניסיון ראשון - JWT מקומי
        try:
            verify_jwt_in_request()
            g.current_user_id = get_jwt_identity()
            g.auth_provider = "local"
            return fn(*args, **kwargs)
        except Exception:
            pass

        # ניסיון שני - Auth0
        try:
            token, error = get_token_auth_header()

            if error:
                raise Exception(error)

            payload = verify_auth0_token(token)

            user = get_or_create_auth0_user(payload)
            g.current_user_id = user.id
            g.auth_provider = "auth0"

            return fn(*args, **kwargs)

        except Exception:
            return jsonify({"error": "Unauthorized"}), 401

    return wrapper