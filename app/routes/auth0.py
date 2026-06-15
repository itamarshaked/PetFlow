from flask import Blueprint, jsonify, g

from services.auth0_service import requires_auth

auth0_bp = Blueprint("auth0", __name__)


@auth0_bp.get("/auth0/me")
@requires_auth
def auth0_me():
    return jsonify({
        "message": "Auth0 token is valid",
        "user": {
            "sub": g.auth0_user.get("sub"),
            "email": g.auth0_user.get("email"),
            "name": g.auth0_user.get("name"),
            "aud": g.auth0_user.get("aud"),
            "iss": g.auth0_user.get("iss"),
        }
    })