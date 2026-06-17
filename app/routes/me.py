from flask import Blueprint, jsonify, g

from services.auth_guard import requires_any_auth

me_bp = Blueprint("me", __name__)


@me_bp.get("/me")
@requires_any_auth
def me():
    user = g.current_user

    return jsonify({
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "auth_provider": user.auth_provider,
        "external_id": user.external_id,
    })