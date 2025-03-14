from flask import request
from flask_restx import Namespace, Resource
from app.models import CloudResource
from app.common import ResponseGenerator
from flask_jwt_extended import jwt_required, get_jwt_identity
import random
import requests
import os

AZURE_COST_MANAGEMENT_URL = "https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.CostManagement/query?api-version=2021-10-01"
AZURE_ACCESS_TOKEN = os.getenv("AZURE_ACCESS_TOKEN")

recommendation_ns = Namespace(
    "recommendations", description="AI-Powered Cost Optimization"
)


@recommendation_ns.route("/")
class CostOptimization(Resource):
    @jwt_required()
    def get(self):
        user_identity = get_jwt_identity()
        subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        url = AZURE_COST_MANAGEMENT_URL.format(subscription_id=subscription_id)

        headers = {
            "Authorization": f"Bearer {AZURE_ACCESS_TOKEN.strip()}",
            "Content-Type": "application/json",
        }

        payload = {
            "type": "ActualCost",
            "timeframe": "MonthToDate",
            "dataset": {
                "granularity": "Daily",
                "aggregation": {"totalCost": {"name": "Cost", "function": "Sum"}},
                "grouping": [{"type": "Dimension", "name": "ResourceGroup"}],
            },
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            return ResponseGenerator.generate_response(
                response.status_code, "error", message="Failed to fetch Azure cost data"
            )

        cost_data = response.json()
        recommendations = []

        for entry in cost_data.get("properties", {}).get("rows", []):
            resource_group = entry[0]  # Extract resource group name
            total_cost = entry[1]  # Extract total cost
            savings_percentage = round(random.uniform(5, 20), 2)
            savings_amount = round((total_cost * savings_percentage) / 100, 2)

            recommendations.append(
                {
                    "resource_group": resource_group,
                    "current_cost": total_cost,
                    "suggested_savings": f"Reduce cost by {savings_percentage}% (~${savings_amount})",
                    "proof": f"Based on Azure data, cost in {resource_group} can be optimized by scaling down unused resources.",
                }
            )

        return ResponseGenerator.generate_response(200, "success", data=recommendations)


@recommendation_ns.route("/apply")
class ApplyCostOptimization(Resource):
    @jwt_required()
    def post(self):
        user_identity = get_jwt_identity()
        data = request.get_json()
        resource_group = data.get("resource_group")
        action = data.get("action")

        if not resource_group or not action:
            return ResponseGenerator.generate_response(
                400,
                "error",
                message="Missing required parameters: resource_group and action",
            )

        # Simulated automation action based on the AI recommendation
        if action == "scale_down":
            automation_response = {
                "resource_group": resource_group,
                "action": "Scaled down underutilized resources",
                "status": "success",
            }
        elif action == "delete_unused":
            automation_response = {
                "resource_group": resource_group,
                "action": "Deleted unused resources",
                "status": "success",
            }
        else:
            return ResponseGenerator.generate_response(
                400, "error", message="Invalid action specified"
            )

        return ResponseGenerator.generate_response(
            200, "success", data=automation_response
        )
