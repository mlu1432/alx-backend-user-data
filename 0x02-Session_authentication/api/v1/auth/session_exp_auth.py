#!/usr/bin/env python3
"""
SessionExpAuth module for managing session authentication with expiration.
"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta

class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth handles session authentication with session expiration.
    Inherits from SessionAuth.
    """
    
    def __init__(self):
        """
        Initializes the session expiration duration.
        """
        session_duration = getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session and stores the session creation time.

        Args:
            user_id (str): The user ID to create a session for.

        Returns:
            str: The session ID or None if the session couldn't be created.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the user ID for a given session ID, considering
        session expiration.

        Args:
            session_id (str): The session ID to get the user ID for.

        Returns:
            str: The user ID or None if session is expired or invalid.
        """
        if session_id is None:
            return None
        
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        
        user_id = session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        
        if self.session_duration <= 0:
            return user_id

        if created_at is None:
            return None
        
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None
        
        return user_id
