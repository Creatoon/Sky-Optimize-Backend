from flask import request
from flask_restx import Namespace, Resource
from app.extensions import db
from app.models import CloudResource
from app.common import ResponseGenerator
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid

resource_ns = Namespace("resources", description="Cloud Resource Management APIs")


# Cloud Resource Management API
@resource_ns.route("/")
class ResourceList(Resource):
    @jwt_required()
    def get(self):
        user_identity = get_jwt_identity()
        resources = CloudResource.query.filter_by(
            tenant_id=user_identity["tenant_id"]
        ).all()
        resource_list = [
            {
                "id": r.id,
                "resource_name": r.resource_name,
                "resource_type": r.resource_type,
                "cost": r.cost,
            }
            for r in resources
        ]
        return ResponseGenerator.generate_response(200, "success", data=resource_list)

    @jwt_required()
    def post(self):
        user_identity = get_jwt_identity()
        data = request.get_json()
        new_resource = CloudResource(
            id=str(uuid.uuid4()),
            tenant_id=user_identity["tenant_id"],
            resource_name=data["resource_name"],
            resource_type=data["resource_type"],
            cost=data["cost"],
        )
        db.session.add(new_resource)
        db.session.commit()
        return ResponseGenerator.generate_response(
            201, "success", message="Cloud resource added successfully"
        )


@resource_ns.route("/<string:resource_id>")
class ResourceDetail(Resource):
    @jwt_required()
    def delete(self, resource_id):
        user_identity = get_jwt_identity()
        resource = CloudResource.query.filter_by(
            id=resource_id, tenant_id=user_identity["tenant_id"]
        ).first()
        if not resource:
            return ResponseGenerator.generate_response(
                404, "error", message="Resource not found"
            )
        db.session.delete(resource)
        db.session.commit()
        return ResponseGenerator.generate_response(
            200, "success", message="Resource deleted successfully"
        )
