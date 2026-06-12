from database import db
from models import Pet


def create_pet_for_user(user_id: str, data: dict) -> Pet:
    pet = Pet(
        name=data.get("name"),
        species=data.get("species"),
        breed=data.get("breed"),
        gender=data.get("gender"),
        age=data.get("age"),
        color=data.get("color"),
        description=data.get("description"),
        chip_number=data.get("chip_number"),
        created_by=user_id
    )

    db.session.add(pet)
    db.session.commit()

    return pet


def get_pet_for_owner(pet_id: str, user_id: str) -> Pet | None:
    return Pet.query.filter_by(id=pet_id, created_by=user_id).first()


def update_pet_image(pet: Pet, image_url: str) -> Pet:
    pet.image_url = image_url
    db.session.commit()
    return pet
