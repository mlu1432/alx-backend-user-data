#!/usr/bin/env python3
"""
Flask app for user authentication and session management.
"""

from flask import Flask, jsonify, request
from auth import Auth

# Initialize Flask app and Auth instance
app = Flask(__name__)
AUTH = Auth()

# Basic GET route for '/'
@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """
    GET route to return a welcome message.

    Returns:
        str: JSON response with message 'Bienvenue'.
    """
    return jsonify({"message": "Bienvenue"}), 200

# POST /users route for registering a new user
@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """
    POST route to register a new user.

    Expects form data: 'email' and 'password'.
    If the user is successfully created, returns a message indicating success.
    If the user is already registered, returns an error message.

    Returns:
        str: JSON response with a success or error message.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # Try to register the user
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        # If the user already exists, return error
        return jsonify({"message": "email already registered"}), 400

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
