#!/usr/bin/env python3
"""
SessionAuth module for managing session authentication.
"""

from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    A class to manage session authentication.
    Currently, this class is empty and inherits from Auth.
    """

    # Class attribute to store user IDs by session IDs
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a given user ID.

        Args:
            user_id (str): The user ID for whom the session is being created.

        Returns:
            str: The session ID or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a unique session ID
        session_id = str(uuid.uuid4())

        # Store the session ID in the dictionary with the user_id as the value
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve the user ID associated with the given session ID.

        Args:
            session_id (str): The session ID to retrieve the user ID for.

        Returns:
            str: The user ID associated with the session ID or None if invalid.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves a User instance based on the session cookie in the request.

        Args:
            request: The Flask request object.

        Returns:
            User: The User instance if found, None otherwise.
        """
        session_id = self.session_cookie(request)
        print(f"Session ID from cookie: {session_id}")
        user_id = self.user_id_for_session_id(session_id)
        print(f"User ID found: {user_id}")
    
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the user session / logs out the user.

        Args:
            request: The Flask request object.

        Returns:
            bool: True if the session was successfully deleted,False otherwise
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        if self.user_id_for_session_id(session_id) is None:
            return False

        # Remove the session from the dictionary
        del self.user_id_by_session_id[session_id]
        return True
