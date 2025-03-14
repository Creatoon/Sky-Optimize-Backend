from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import User
from app.common import ResponseGenerator
import uuid


# Define Namespace
auth_ns = Namespace("auth", description="Authentication APIs")

# Request Models
signup_model = auth_ns.model(
    "Signup",
    {
        "name": fields.String(required=True, description="Full name"),
        "email": fields.String(required=True, description="Email address"),
        "password": fields.String(required=True, description="Password"),
        "tenant_id": fields.String(required=True, description="Tenant ID"),
    },
)

login_model = auth_ns.model(
    "Login",
    {
        "email": fields.String(required=True, description="Email address"),
        "password": fields.String(required=True, description="Password"),
    },
)


# API Resources
@auth_ns.route("/signup")
class Signup(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()
        existing_user = User.query.filter_by(email=data["email"]).first()

        if existing_user:
            return ResponseGenerator.generate_response(
                400, "error", message="User already exists"
            )

        hashed_password = generate_password_hash(data["password"])
        new_user = User(
            id=str(uuid.uuid4()),
            tenant_id=data["tenant_id"],
            name=data["name"],
            email=data["email"],
            password_hash=hashed_password,
            role="viewer",  # Default role
        )

        db.session.add(new_user)
        db.session.commit()

        return ResponseGenerator.generate_response(
            201, "success", message="User created successfully"
        )


@auth_ns.route("/login")
class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data["email"]).first()

        if not user or not check_password_hash(user.password_hash, data["password"]):
            return ResponseGenerator.generate_response(
                401, "error", message="Invalid credentials"
            )

        access_token = create_access_token(identity=str(user.id))
        return ResponseGenerator.generate_response(
            200, "success", data={"access_token": access_token}
        )


@auth_ns.route("/profile")
class Profile(Resource):
    @jwt_required()
    def get(self):
        user_identity = get_jwt_identity()
        user = User.query.get(user_identity["id"])

        if not user:
            return ResponseGenerator.generate_response(
                404, "error", message="User not found"
            )

        return ResponseGenerator.generate_response(
            200,
            "success",
            data={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "tenant_id": user.tenant_id,
            },
        )
