import uuid
from datetime import datetime

from database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Pet(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120), nullable=False)

    species = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(120), nullable=True)
    gender = db.Column(db.String(40), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    color = db.Column(db.String(80), nullable=True)
    description = db.Column(db.Text, nullable=True)

    chip_number = db.Column(db.String(64), nullable=True, unique=True)
    image_url = db.Column(db.String(512), nullable=True)

    created_by = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "gender": self.gender,
            "age": self.age,
            "color": self.color,
            "description": self.description,
            "chip_number": self.chip_number,
            "has_image": self.image_url is not None,
            "image_url": self.image_url,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
