from flask import Blueprint, jsonify

docs_bp = Blueprint("docs", __name__)


@docs_bp.get("/openapi.json")
def openapi():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "PetFlow API",
            "version": "1.0.0"
        },
        "paths": {
            "/health": {"get": {"summary": "Health check"}},
            "/register": {"post": {"summary": "Register user"}},
            "/login": {"post": {"summary": "Login user"}},
            "/pets": {
                "get": {"summary": "List pets"},
                "post": {"summary": "Create pet"}
            },
            "/pets/{pet_id}": {
                "get": {"summary": "Get pet by ID"},
                "put": {"summary": "Update pet"},
                "delete": {"summary": "Delete pet"}
            },
            "/pets/{pet_id}/image": {
                "post": {"summary": "Upload pet image"}
            }
        }
    })
