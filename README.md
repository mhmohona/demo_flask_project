# Cerbos Flask Demo Project

## Overview

This project is a demo application showcasing how to use the Cerbos authorization engine within a Python Flask application. The project aims to demonstrate Cerbos's role-based access control (RBAC) features by allowing users with different roles to access, edit, or delete content on a dashboard. The project is developed with simplicity and clarity in mind, making it an ideal sample for those interested in Cerbos integrations.

The following technologies are used in this demo:

- Flask for the web framework.
- Cerbos as the policy engine to manage role-based authorization.
- HTML for creating simple templates with Bootstrap for styling.
- Python for server-side logic.

For more details on the authorization implementation, check out my blog post: [Adding Authorization to a Flask App](https://medium.com/@mhmohona/adding-authorization-to-your-flask-app-a-beginners-guide-66d48db11176)

## Features

- **Role-based Access Control**: Users are assigned different roles (Guest, Viewer, Editor, Admin) which dictate their access to various actions such as viewing, editing, or deleting the dashboard content.
- **Cerbos Integration**: The Flask app makes use of Cerbos policies to determine the access rights of different roles.
- **User-friendly Dashboard**: The project features a simple dashboard with role-specific actions that are enabled or disabled based on the user's permissions.

## Folder Structure

- **app.py**: Main Flask application file containing route definitions and application logic. Routes include home (`/`) and dashboard (`/dashboard`) views, as well as endpoints for editing and deleting dashboard content.
- **cerbos_service.py**: Contains functions to interact with the Cerbos authorization service, including payload construction and API request handling.
- **resources.py**: Stores information on users, their roles, and other relevant resources for easy reference and integration.
- **templates/index.html**: The home page where users can select a role and navigate to the dashboard.
- **templates/dashboard.html**: The dashboard view which displays content and action buttons based on user roles.

## Setup Instructions

### Installation

First, install cerbos following the [documentation](https://docs.cerbos.dev/cerbos/latest/installation/binary). 

1. Clone this repository:
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application
1. Start the Flask server:
    ```bash
    python app.py
    ```
2. Open your browser and navigate to `http://127.0.0.1:5000` to access the home page.

3. Use the links on the homepage to simulate different roles and test the access control features on the dashboard.

## Usage
- **Home Page**: From the home page (`index.html`), users can navigate to the dashboard while choosing different roles (Guest, Viewer, Editor, Admin). Each role provides different levels of access.
- **Dashboard Page**: The dashboard shows the current content and allows the user to perform actions based on their role. For example, users with the `admin` or `editor` roles can edit or delete the content, whereas a `viewer` can only view.

### Role-specific URLs for Dashboard Access
- **Admin role** [Admin Dashboard](http://127.0.0.1:5000/dashboard?role=admin) 

  Can view, edit, and delete the dashboard content.

  ![image](https://github.com/user-attachments/assets/81241fda-bb93-4390-b96d-7db4be36bf6e)

- **Editor role**: [Editor Dashboard](http://127.0.0.1:5000/dashboard?role=editor)
  Can view and edit the dashboard content.

  ![image](https://github.com/user-attachments/assets/0e162c46-1972-4746-a1d4-b418da49c709)

- **Viewer role**: [Viewer Dashboard](http://127.0.0.1:5000/dashboard?role=viewer)
  Can only view the dashboard content.

  ![image](https://github.com/user-attachments/assets/a913a7a5-3872-414e-914b-203ae3737927)


- **Restricted role**: [Restricted Dashboard](http://127.0.0.1:5000/dashboard?role=restricted)
  Cannot access the dashboard.

  ![image](https://github.com/user-attachments/assets/389fffc4-7d87-4ea9-af2e-8bcc9f6d5fc8)

- **Guest role**: [Guest Dashboard](http://127.0.0.1:5000/dashboard?role=guest)
  Can view but cannot edit or delete.

  ![image](https://github.com/user-attachments/assets/a871a171-cc60-450d-b8ef-cc0f25055e8e)


## How Cerbos Is Used
- The **`is_authorized`** function in [`cerbos_service.py`](cerbos_service.py) interacts with Cerbos to check if a user has permission to perform a specific action.
- Cerbos is used to implement role-based access control (RBAC). The Flask application sends requests to the Cerbos policy engine to determine if a particular user can perform an action on a given resource. This enables fine-grained permissions without embedding complex logic directly in the application code.

## Policy File ([`resource_policy.yaml`](cerbos-policies/policies/resource_policy.yaml))

The Cerbos policy file defines which actions each role can perform on the `dashboard` resource:
- **`view` action**: Allowed for all roles (`admin`, `editor`, `viewer`, `guest`), meaning that any user can access the dashboard.
- **`edit` action**: Allowed for `admin` and `editor` roles. Only these roles can modify the dashboard content.
- **`delete` action**: Allowed only for `admin` role. Only admins have permission to delete the dashboard content.
- **Restricted role**: Users with the `restricted` role are explicitly denied viewing access to the dashboard.

The policy works by evaluating the user's role against the defined rules for each action (`view`, `edit`, `delete`) on the `dashboard` resource. Cerbos processes the request, checking if the user's role matches the conditions specified in the policy, and then either grants or denies the action. This approach ensures that the access control logic is separated from the application code, making it easier to manage and update permissions as needed.
