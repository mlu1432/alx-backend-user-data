#!/usr/bin/env python3
"""
Auth module to manage authentication.
"""

from db import DB
from user import User
import bcrypt
from typing import TypeVar


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize Auth with a private DB instance."""
        self._db = DB()

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with the given email and password.

        Args:
            email (str): The email of the new user.
            password (str): The password of the new user.

        Returns:
            User: The newly created user.

        Raises:
            ValueError: If the user already exists.
        """
        # Check if a user with the given email already exists
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except Exception:
            # If no user is found, proceed to register the new user
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(
                email=email,
                hashed_password=hashed_password
            )
            return new_user
