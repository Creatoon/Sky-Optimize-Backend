from flask import request
from flask_restx import Namespace, Resource
from app.extensions import db
from app.models import Tenant
from app.common import ResponseGenerator
from app.decorators import role_required
import uuid

tenant_ns = Namespace("tenants", description="Tenant Management APIs")


# Tenant Management API
@tenant_ns.route("/")
class TenantList(Resource):
    @role_required(["admin"])
    def get(self):
        tenants = Tenant.query.all()
        tenant_list = [{"id": t.id, "name": t.name} for t in tenants]
        return ResponseGenerator.generate_response(200, "success", data=tenant_list)

    @role_required(["admin"])
    def post(self):
        data = request.get_json()
        new_tenant = Tenant(id=str(uuid.uuid4()), name=data["name"])
        db.session.add(new_tenant)
        db.session.commit()
        return ResponseGenerator.generate_response(
            201, "success", message="Tenant created successfully"
        )


@tenant_ns.route("/<string:tenant_id>")
class TenantResource(Resource):
    @role_required(["admin"])
    def delete(self, tenant_id):
        tenant = Tenant.query.get(tenant_id)
        if not tenant:
            return ResponseGenerator.generate_response(
                404, "error", message="Tenant not found"
            )
        db.session.delete(tenant)
        db.session.commit()
        return ResponseGenerator.generate_response(
            200, "success", message="Tenant deleted successfully"
        )
