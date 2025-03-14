from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import requests
from app.common import ResponseGenerator

# Define Namespace
cost_ns = Namespace("cost", description="Azure Cost Management Integration")

# Azure Cost Management API Integration
AZURE_COST_MANAGEMENT_URL = "https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.CostManagement/query?api-version=2021-10-01"
AZURE_ACCESS_TOKEN = os.getenv("AZURE_ACCESS_TOKEN")  # Store in environment variables


@cost_ns.route("/")
class AzureCost(Resource):
    @jwt_required()
    def get(self):
        user_identity = get_jwt_identity()
        subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        url = AZURE_COST_MANAGEMENT_URL.format(subscription_id=subscription_id)

        headers = {
            "Authorization": f"Bearer {AZURE_ACCESS_TOKEN}",
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

        data = response.json()
        return ResponseGenerator.generate_response(200, "success", data=data)
