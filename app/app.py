from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from config import Config
from database import db

from routes.health import health_bp
from routes.auth import auth_bp
from routes.pets import pets_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    JWTManager(app)
    Migrate(app, db)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(pets_bp)

    return app


app = create_app()