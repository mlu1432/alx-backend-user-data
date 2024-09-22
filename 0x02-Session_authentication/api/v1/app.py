#!/usr/bin/env python3
"""
App module for the Flask application.
"""

from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth to None
auth = None

# Check the AUTH_TYPE environment variable and instantiate the appropriate class
auth_type = getenv("AUTH_TYPE", None)

if auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "session_auth":
    auth = SessionAuth()
else:
    auth = Auth()

@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized error handler"""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden error handler"""
    return jsonify({"error": "Forbidden"}), 403

@app.before_request
def before_request():
    """Method to handle all requests before processing"""
    if auth is None:
        pass
    else:
        request.current_user = auth.current_user(request)
        excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                          '/api/v1/forbidden/', '/api/v1/auth_session/login/']
        if not auth.require_auth(request.path, excluded_paths):
            return
        if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
            abort(401)
        if auth.current_user(request) is None:
            abort(403)

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
