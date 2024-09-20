#!/usr/bin/env python3
"""
Auth class for managing API authentication.
"""

from typing import List, TypeVar
from flask import request


class Auth:
    """
    A class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.

        Parameters:
        path (str): The path to check.
        excluded_paths (List[str]): List of paths that don't require authentication.

        Returns:
        bool: True if authentication is required, False otherwise.
        """
        # If path is None or excluded_paths is None or empty, return True
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure the path ends with a slash for comparison
        if not path.endswith('/'):
            path += '/'

        # Check if the path is in excluded_paths
        for ex_path in excluded_paths:
            if ex_path.endswith('/') and path == ex_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the Flask request object.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.
        """
        return None
