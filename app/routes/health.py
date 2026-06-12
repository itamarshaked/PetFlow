from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/")
def home():
    return jsonify({
        "app": "PetFlow",
        "status": "running",
        "platform": "EKS"
    })


@health_bp.get("/health")
def health():
    return jsonify({"status": "healthy"})
