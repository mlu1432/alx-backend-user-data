#!/usr/bin/env python3
"""
Auth class for managing the API authentication.
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    A class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'
        if path in excluded_paths:
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
