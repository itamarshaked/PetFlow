from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from models import User
from services.auth_service import create_user, verify_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "user already exists"}), 409

    user = create_user(email, password)

    return jsonify({
        "message": "user created",
        "user_id": user.id
    }), 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    user = verify_user(email, password)

    if not user:
        return jsonify({"error": "invalid credentials"}), 401

    token = create_access_token(identity=user.id)

    return jsonify({"access_token": token})
