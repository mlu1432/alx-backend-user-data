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
        Determines if authentication is required for a given path.
        For now, always returns False.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.
        For now, always returns None.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user.
        For now, always returns None.
        """
        return None
