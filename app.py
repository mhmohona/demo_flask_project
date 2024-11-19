from flask import Flask, render_template, request, redirect, url_for
import logging
from cerbos_service import is_authorized

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    if not can_view:
        return render_template('dashboard.html', cerbos_status="Access denied - Cerbos authorization failed"), 403

    can_edit = is_authorized(user, "edit", "dashboard")
    can_delete = is_authorized(user, "delete", "dashboard")

    return render_template(
        'dashboard.html',
        cerbos_status="Running",
        role=user["roles"][0],
        can_edit=can_edit,
        can_delete=can_delete,
        dashboard_content=dashboard_content
    )

@app.route('/edit_dashboard', methods=['POST'])
def edit_dashboard():
    role = request.args.get('role', 'guest')
    user = {
        "id": "user1",
        "roles": [role]
    }

    # Check if the user is authorized to edit
    if is_authorized(user, "edit", "dashboard"):
        edited_content = request.form.get("edited_content")
        if edited_content:
            global dashboard_content
            dashboard_content = edited_content
            return redirect(url_for('dashboard', role=role))
    return "Access Denied - You do not have permission to edit the dashboard", 403

@app.route('/delete_dashboard', methods=['POST'])
def delete_dashboard():
    role = request.args.get('role', 'guest')
    user = {
        "id": "user1",
        "roles": [role]
    }

    # Check if the user is authorized to delete
    if is_authorized(user, "delete", "dashboard"):
        global dashboard_content
        dashboard_content = "Content has been deleted."
        return redirect(url_for('dashboard', role=role))
    return "Access Denied - You do not have permission to delete the dashboard", 403

# Variable to simulate dashboard content
dashboard_content = "This is the original dashboard content."

if __name__ == "__main__":
    app.run(debug=True)
