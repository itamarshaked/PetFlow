from functools import wraps

from flask import g, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from models import User
from services.auth0_service import get_token_auth_header, verify_auth0_token
from services.user_service import get_or_create_auth0_user


def requires_any_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            g.current_user_id = user_id
            g.current_user = user
            g.current_user_role = user.role if user else "user"
            g.auth_provider = "local"

            return fn(*args, **kwargs)
        except Exception:
            pass

        try:
            token, error = get_token_auth_header()
            if error:
                raise Exception(error)

            payload = verify_auth0_token(token)
            user = get_or_create_auth0_user(payload)

            g.current_user_id = user.id
            g.current_user = user
            g.current_user_role = user.role
            g.auth_provider = "auth0"

            return fn(*args, **kwargs)

        except Exception as exc:
            return jsonify({
                "error": "Unauthorized",
                "details": str(exc)
            }), 401

    return wrapper