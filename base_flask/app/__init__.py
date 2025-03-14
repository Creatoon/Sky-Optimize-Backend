from flask import Flask
from flask_migrate import Migrate
from .config import Config
from .extensions import db, jwt, api
from .routes.auth import auth_ns
from .routes.tenants import tenant_ns
from .routes.resources import resource_ns
from .routes.recommendations import recommendation_ns
from .routes.cost import cost_ns

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app)

    # Register Namespaces
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(tenant_ns, path="/tenants")
    api.add_namespace(resource_ns, path="/resources")
    api.add_namespace(cost_ns, path="/cost")
    api.add_namespace(recommendation_ns, path="/recommendations")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
