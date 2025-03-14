from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common import ResponseGenerator


# Role-Based Access Control (RBAC) Decorator
def role_required(required_roles):
    def decorator(fn):
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_identity = get_jwt_identity()
            if user_identity["role"] not in required_roles:
                return ResponseGenerator.generate_response(
                    403, "error", message="Access forbidden: Insufficient role"
                )
            return fn(*args, **kwargs)

        return wrapper

    return decorator
