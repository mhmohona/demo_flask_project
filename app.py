# app.py

from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

CERBOS_URL = "http://localhost:3592/api/check"

def is_authorized(user, action, resource):
    payload = {
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

    response = requests.post(CERBOS_URL, json=payload)
    response_data = response.json()

    # Debug print to see the full response from Cerbos
    print("Cerbos Response:", response_data)

    if "resourceInstances" in response_data and "instance_id" in response_data["resourceInstances"]:
        return response_data["resourceInstances"]["instance_id"]["actions"][action] == "EFFECT_ALLOW"
    else:
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    role = request.args.get('role', 'guest')
    user = {
        "id": "user1",
        "roles": [role]
    }

    # Check if the user is authorized for different actions
    can_view = is_authorized(user, "view", "dashboard")
    can_edit = is_authorized(user, "edit", "dashboard")
    can_delete = is_authorized(user, "delete", "dashboard")

    if can_view:
        return render_template(
            'dashboard.html',
            cerbos_status="Running",
            role=user["roles"][0],
            can_edit=can_edit,
            can_delete=can_delete
        )
    else:
        return render_template('dashboard.html', cerbos_status="Access denied - Cerbos authorization failed"), 403

# New route to edit dashboard content
@app.route('/edit_dashboard', methods=['POST'])
def edit_dashboard():
    role = request.args.get('role', 'guest')
    user = {
        "id": "user1",
        "roles": [role]
    }

    # Check if the user is authorized to edit
    if is_authorized(user, "edit", "dashboard"):
        # Simulate editing logic here (e.g., updating a value)
        edited_content = request.form.get("edited_content")
        # For simplicity, we'll store edited content in a variable
        global dashboard_content
        dashboard_content = edited_content
        return redirect(url_for('dashboard', role=role))
    else:
        return "Access Denied - You do not have permission to edit the dashboard", 403

# New route to delete dashboard content
@app.route('/delete_dashboard', methods=['POST'])
def delete_dashboard():
    role = request.args.get('role', 'guest')
    user = {
        "id": "user1",
        "roles": [role]
    }

    # Check if the user is authorized to delete
    if is_authorized(user, "delete", "dashboard"):
        # Simulate delete logic here (e.g., resetting content)
        global dashboard_content
        dashboard_content = "Content has been deleted."
        return redirect(url_for('dashboard', role=role))
    else:
        return "Access Denied - You do not have permission to delete the dashboard", 403

# Variable to simulate dashboard content
dashboard_content = "This is the original dashboard content."
if __name__ == "__main__":
    app.run(debug=True)