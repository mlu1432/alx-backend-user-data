#!/usr/bin/env python3
"""
SessionAuth module for managing session authentication.
"""

from api.v1.auth.auth import Auth
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
