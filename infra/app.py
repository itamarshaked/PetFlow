import os
import uuid
from datetime import timedelta

import bcrypt
import boto3
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Pet(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.String(512), nullable=True)
    created_by = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

def create_app():
    app = Flask(__name__)

    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME", "petflow")
    db_user = os.getenv("DB_USER", "petflow_admin")
    db_password = os.getenv("DB_PASSWORD")
    jwt_secret = os.getenv("JWT_SECRET", "change-me-in-production")
    s3_bucket = os.getenv("S3_BUCKET")
    aws_region = os.getenv("AWS_REGION", "eu-central-1")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = jwt_secret
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)

    db.init_app(app)
    JWTManager(app)

    s3_client = boto3.client("s3", region_name=aws_region)

    with app.app_context():
        db.create_all()

    @app.get("/")
    def home():
        return jsonify({
            "app": "PetFlow",
            "status": "running",
            "platform": "EKS"
        })

    @app.get("/health")
    def health():
        return jsonify({"status": "healthy"})

    @app.post("/register")
    def register():
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "email and password are required"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "user already exists"}), 409

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User(email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "user created", "user_id": user.id}), 201

    @app.post("/login")
    def login():
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return jsonify({"error": "invalid credentials"}), 401

        token = create_access_token(identity=user.id)
        return jsonify({"access_token": token})

    @app.get("/pets")
    def list_pets():
        pets = Pet.query.all()
        return jsonify([
            {
                "id": pet.id,
                "name": pet.name,
                "type": pet.type,
                "age": pet.age,
                "image_url": pet.image_url,
                "created_by": pet.created_by
            }
            for pet in pets
        ])

    @app.post("/pets")
    @jwt_required()
    def create_pet():
        user_id = get_jwt_identity()
        data = request.get_json() or {}

        name = data.get("name")
        pet_type = data.get("type")
        age = data.get("age")

        if not name or not pet_type:
            return jsonify({"error": "name and type are required"}), 400

        pet = Pet(
            name=name,
            type=pet_type,
            age=age,
            created_by=user_id
        )

        db.session.add(pet)
        db.session.commit()

        return jsonify({
            "message": "pet created",
            "pet_id": pet.id
        }), 201

    @app.post("/pets/<pet_id>/image")
    @jwt_required()
    def upload_pet_image(pet_id):
        user_id = get_jwt_identity()

        if "image" not in request.files:
            return jsonify({"error": "image file is required"}), 400

        pet = Pet.query.filter_by(id=pet_id, created_by=user_id).first()
        if not pet:
            return jsonify({"error": "pet not found"}), 404

        image = request.files["image"]
        file_ext = image.filename.rsplit(".", 1)[-1].lower() if "." in image.filename else "jpg"
        object_key = f"pets/{pet_id}/{uuid.uuid4()}.{file_ext}"

        s3_client.upload_fileobj(
            image,
            s3_bucket,
            object_key,
            ExtraArgs={"ContentType": image.content_type}
        )

        pet.image_url = f"s3://{s3_bucket}/{object_key}"
        db.session.commit()

        return jsonify({
            "message": "image uploaded",
            "image_url": pet.image_url
        }), 201

    return app

app = create_app()
