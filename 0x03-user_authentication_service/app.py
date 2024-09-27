#!/usr/bin/env python3
"""
Flask app for user authentication and session management.
"""

from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """
    GET route to return a welcome message.

    Returns:
        str: JSON response with message 'Bienvenue'.
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def user() -> str:
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
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    POST route to log in a user and create a session.

    Expects form data: 'email' and 'password'.
    If login is successful, returns a session ID cookie.
    If login fails, returns a 401 error.

    Returns:
        str: JSON response with a success message.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if not valid_login:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    DELETE route to log out a user and destroy their session.

    Expects the session ID from cookies.
    If the session is valid, logs the user out and redirects to the homepage.
    If the session is invalid, returns a 403 error.

    Returns:
        str: Redirect to the homepage or 403 error.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    GET route to retrieve the profile information of the logged-in user.

    Expects the session ID from cookies.
    If the session is valid, returns the user's email.
    If the session is invalid, returns a 403 error.

    Returns:
        str: JSON response with the user's email or a 403 error.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    POST route to generate a password reset token for a user.

    Expects form data: 'email'.
    If the user exists, returns the reset token.
    If the user does not exist, returns a 403 error.

    Returns:
        str: JSON response with the reset token or a 403 error.
    """
    email = request.form.get('email')
    user = AUTH.create_session(email)
    if not user:
        abort(403)
    else:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    PUT route to update a user's password using a reset token.

    Expects form data: 'email', 'reset_token', and 'new_password'.
    If the token is valid, updates the password and returns a success message.
    If the token is invalid, returns a 403 error.

    Returns:
        str: JSON response with a success message or a 403 error.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
