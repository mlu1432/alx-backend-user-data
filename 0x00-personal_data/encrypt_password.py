#!/usr/bin/env python3
"""
Module for password hashing and validation using bcrypt.
"""

import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with a generated salt.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        bytes: The salted, hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password by comparing it to the hashed password.

    Args:
        hashed_password (bytes): The hashed password to compare against.
        password (str): The plain-text password to check.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
