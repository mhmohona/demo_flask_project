import requests
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CERBOS_URL = os.getenv("CERBOS_URL", "http://localhost:3592/api/check")

def construct_payload(user, action, resource):
    return {
        "requestId": "flask_request",
        "principal": {
            "id": user["id"],
            "roles": user["roles"],
            "attr": user.get("attributes", {})
        },
        "resource": {
            "kind": resource,
            "instances": {
                "instance_id": {
                    "attr": {}
                }
            }
        },
        "actions": [action]
    }

def call_cerbos_api(payload):
    try:
        response = requests.post(CERBOS_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error("Failed to connect to Cerbos: %s", e)
        return None

def is_authorized(user, action, resource):
    """
    Check if the user is authorized to perform an action on a resource.

    Args:
        user (dict): User details containing id, roles, and attributes.
        action (str): The action to be checked (e.g., 'view', 'edit').
        resource (str): The resource being accessed.

    Returns:
        bool: True if authorized, False otherwise.
    """
    payload = construct_payload(user, action, resource)
    response_data = call_cerbos_api(payload)

    if response_data and "resourceInstances" in response_data and "instance_id" in response_data["resourceInstances"]:
        return response_data["resourceInstances"]["instance_id"]["actions"].get(action) == "EFFECT_ALLOW"
    return False
