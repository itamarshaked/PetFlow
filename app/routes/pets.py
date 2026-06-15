from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import db
from models import Pet
from services.pet_service import create_pet_for_user, get_pet_for_owner, update_pet_image
from services.s3_service import upload_pet_image

pets_bp = Blueprint("pets", __name__)


@pets_bp.get("/pets")
@jwt_required()
def list_pets():
    user_id = get_jwt_identity()
    pets = Pet.query.filter_by(created_by=user_id).all()
    return jsonify([pet.to_dict() for pet in pets])


@pets_bp.get("/pets/<pet_id>")
@jwt_required()
def get_pet(pet_id):
    user_id = get_jwt_identity()
    pet = get_pet_for_owner(pet_id, user_id)

    if not pet:
        return jsonify({"error": "pet not found"}), 404

    return jsonify(pet.to_dict())


@pets_bp.post("/pets")
@jwt_required()
def create_pet():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    if not data.get("name") or not data.get("species"):
        return jsonify({"error": "name and species are required"}), 400

    if data.get("chip_number"):
        existing_pet = Pet.query.filter_by(chip_number=data["chip_number"]).first()
        if existing_pet:
            return jsonify({"error": "chip_number already exists"}), 409

    pet = create_pet_for_user(user_id, data)

    return jsonify({
        "message": "pet created",
        "pet": pet.to_dict()
    }), 201


@pets_bp.put("/pets/<pet_id>")
@jwt_required()
def update_pet(pet_id):
    user_id = get_jwt_identity()
    pet = get_pet_for_owner(pet_id, user_id)

    if not pet:
        return jsonify({"error": "pet not found"}), 404

    data = request.get_json() or {}

    for field in [
        "name",
        "species",
        "breed",
        "gender",
        "age",
        "color",
        "description",
        "chip_number",
    ]:
        if field in data:
            setattr(pet, field, data[field])

    db.session.commit()

    return jsonify({
        "message": "pet updated",
        "pet": pet.to_dict()
    })


@pets_bp.delete("/pets/<pet_id>")
@jwt_required()
def delete_pet(pet_id):
    user_id = get_jwt_identity()
    pet = get_pet_for_owner(pet_id, user_id)

    if not pet:
        return jsonify({"error": "pet not found"}), 404

    db.session.delete(pet)
    db.session.commit()

    return jsonify({"message": "pet deleted"})


@pets_bp.post("/pets/<pet_id>/image")
@jwt_required()
def upload_image(pet_id):
    user_id = get_jwt_identity()
    pet = get_pet_for_owner(pet_id, user_id)

    print("=" * 60)
    print("JWT Identity :", repr(user_id))
    print("Pet ID       :", repr(pet_id))
    print("Pet Found    :", pet is not None)
    print("=" * 60)

    print("JWT identity:", get_jwt_identity())

    if not pet:
        return jsonify({"error": "pet not found"}), 404

    if "file" not in request.files:
        return jsonify({"error": "image file is required"}), 400

    image_url = upload_pet_image(request.files["file"], pet.id)
    pet = update_pet_image(pet, image_url)

    return jsonify({
        "message": "image uploaded",
        "pet": pet.to_dict()
    }), 201
