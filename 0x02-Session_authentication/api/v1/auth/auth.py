#!/usr/bin/env python3
"""
Auth class for managing the API authentication.
"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    A class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.

        Args:
            path (str): The request path.
            excluded_paths (List[str]): A list of paths that do not require
            authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            # Handle wildcards: if the excluded path ends with "*"
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.

        Parameters:
        request: The Flask request object.

        Returns:
        str: The value of the Authorization header, or None if not present.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.

        Parameters:
        request: The Flask request object.

        Returns:
        TypeVar('User'): Always None for now.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie from the request.

        Args:
            request: The Flask request object.

        Returns:
            The session ID from the cookie named based on SESSION_NAME.
        """
        if request is None:
            return None

        session_name = getenv("SESSION_NAME")
        if session_name is None:
            return None

        return request.cookies.get(session_name)
