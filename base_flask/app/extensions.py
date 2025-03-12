from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restx import Api

db = SQLAlchemy()
jwt = JWTManager()
api = Api(
    title="Sky Optimize API",
    version="1.0",
    description="Multi-Tenant Cost Optimization",
)
