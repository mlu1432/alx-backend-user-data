#!/usr/bin/env python3
"""
BasicAuth class for managing basic authentication.
"""

import base64
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    A class to manage Basic Authentication.
    Inherits from Auth.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header from the request.

        Returns:
            str: The Base64 part of the Authorization header if valid, otherwise None.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 string to a UTF-8 string.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: The decoded UTF-8 string, or None if invalid input or decoding error.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user credentials from the decoded Base64 authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64 string.

        Returns:
            tuple: The user email and password if valid, otherwise (None, None).
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str):
        """
        Returns the User instance based on email and password.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            User instance if credentials are valid, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users or len(users) == 0:
            return None

        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> User:
        """
        Retrieves the User instance for a request using Basic Authentication.

        Args:
            request: The Flask request object.

        Returns:
            The authenticated User instance or None if no valid credentials.
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_auth_header = self.extract_base64_authorization_header(auth_header)
        if base64_auth_header is None:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(base64_auth_header)
        if decoded_auth_header is None:
            return None

        email, password = self.extract_user_credentials(decoded_auth_header)
        if email is None or password is None:
            return None

        return self.user_object_from_credentials(email, password)
