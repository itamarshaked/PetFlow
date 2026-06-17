from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from config import Config
from database import db
from routes.auth import auth_bp
from routes.auth0 import auth0_bp
from routes.docs import docs_bp
from routes.health import health_bp
from routes.pets import pets_bp
from prometheus_flask_exporter import PrometheusMetrics
from routes.me import me_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)
    Migrate(app, db)
    PrometheusMetrics(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(auth0_bp)
    app.register_blueprint(pets_bp)
    app.register_blueprint(docs_bp)
    app.register_blueprint(me_bp)

    return app


app = create_app()
