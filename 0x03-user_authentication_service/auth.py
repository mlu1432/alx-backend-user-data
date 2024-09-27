#!/usr/bin/env python3
"""
Auth module for user authentication.
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
        """Register a new user and save them to the database."""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except Exception:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(
                email=email,
                hashed_password=hashed_password
            )
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate credentials for login.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            bool: True if valid credentials, False otherwise.
        """
        try:
            # Locate the user by email
            user = self._db.find_user_by(email=email)
            # Check if the password matches using bcrypt
            return bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password.encode('utf-8')
            )
        except Exception:
            return False
