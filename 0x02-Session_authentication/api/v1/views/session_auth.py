#!/usr/bin/env python3
"""
View for handling session authentication.
"""

from flask import jsonify, request, abort
from models.user import User
from api.v1.views import app_views
from os import getenv

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handles session authentication login."""
    from api.v1.app import auth

    # Retrieve email and password from the request form
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is provided
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check if password is provided
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for the user with the provided email
    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if the password matches
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session for the user
    session_id = auth.create_session(user.id)
    if session_id is None:
        abort(500)

    # Set the session ID as a cookie in the response
    session_name = getenv("SESSION_NAME")
    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)

    return response
