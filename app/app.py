from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

from config import Config
from database import db
from routes.auth import auth_bp
from routes.docs import docs_bp
from routes.health import health_bp
from routes.pets import pets_bp
from prometheus_flask_exporter import PrometheusMetrics


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)
    Migrate(app, db)
    PrometheusMetrics(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(pets_bp)
    app.register_blueprint(docs_bp)

    swagger_ui = get_swaggerui_blueprint(
        "/docs",
        "/openapi.json",
        config={"app_name": "PetFlow API"},
    )

    app.register_blueprint(swagger_ui, url_prefix="/docs")

    return app


app = create_app()
