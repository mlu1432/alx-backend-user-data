#!/usr/bin/env python3
"""
Auth module to handle password hashing.
"""

import bcrypt


def _hash_password(password: str) -> str:
    """
    Hash a password for the user using bcrypt.

    Args:
        password (str): The password of the user.

    Returns:
        str: The salted and hashed password in string format.
    """
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
