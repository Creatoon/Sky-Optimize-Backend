from flask import Flask
from .config import Config
from .extensions import db, jwt, api
from .routes.auth import auth_ns
from .routes.tenants import tenant_ns
from .routes.resources import resource_ns


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    # Register Namespaces
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(tenant_ns, path="/tenants")
    api.add_namespace(resource_ns, path="/resources")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
